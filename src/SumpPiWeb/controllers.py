
import datetime

import threading
import _thread
import time
import datetime
import json

from flask import request
from SumpPiWeb import app
from SumpPiWeb import Alarm, Database, views, config

from SumpPiWeb.cloud_request import SendAlarmDistanceToCloud
from SumpPiWeb.Measurement import Measurement,CustomEncoder
from SumpPiWeb.DailySummaryCalculator import DailySummaryCalculator
from SumpPiWeb.DistanceReader import DistanceReader

start_time = datetime.datetime.now()

db = Database.Database()
dist_rdr = DistanceReader(db)
dist_rdr.start()
		
def end_threads():
	dist_rdr.end_thread = True
	dist_rdr.join()

# Flask web routes
@app.route('/uptime', methods=['GET'])
def get_uptime():
	uptime = datetime.datetime.now() - start_time
	uptime_msg = ""
	if uptime.days > 0:
		uptime_msg = '{} days, {} hours'.format(uptime.days, int(uptime.seconds / 60.0 / 60.0))
	elif uptime.seconds > 3600:
		uptime_msg = '{} hours'.format(int(uptime.seconds / 60.0 / 60.0))
	elif uptime.seconds > 60:
		uptime_msg = '{} minutes'.format(int(uptime.seconds / 60.0))
	else:
		uptime_msg = '{} seconds'.format(uptime.seconds)
	return uptime_msg

@app.route('/alarming', methods=['GET'])
def get_alarming():
    return str(dist_rdr.alarm_system.sound_alarm)


@app.route('/alarm_settings', methods=['GET', 'POST'])
def set_alarming_alarm_settings():
	if request.method == 'GET':
		return json.dumps( {'distance': str(db.read_alarm_distance()),
											'time_in_alarm':str(db.read_alarm_time_in_alarm()),
											'enable_audible_alarm':str(db.read_alarm_enable_audible_alarm())}) 
	else:
		if config.CLOUD:
			return 'not allowed'

		db.store_alarm_distance(float(request.form['distance']))
		db.store_alarm_time_in_alarm(float(request.form['time_in_alarm']))
		db.store_alarm_enable_audible_alarm(request.form['enable_audible_alarm'])
		dist_rdr.alarm_system.audible_alarm_enabled = request.form['enable_audible_alarm'] == 'true'
		
		SendAlarmDistanceToCloud(request.form['distance'])

	return 'success'


@app.route('/depth', methods=['GET'])
def get_depth():

	samples = 300
	if request.args.get('samples') != None:
		samples = int(request.args.get('samples'))

	dist_rdr.thread_lock.acquire()
	response = json.dumps(dist_rdr.depth_series[-int(samples):], cls=CustomEncoder);
	dist_rdr.thread_lock.release()
	return response

@app.route('/daily_summaries', methods=['GET'])
def get_daily_summaries():
	days = 7
	if request.args.get('days') != None:
		days = int(request.args.get('days'))
	now = datetime.datetime.now()
	times=[]
	labels=[]
	for i in range(days, 0, -1):
		d = now + datetime.timedelta(-i)
		times.append(d.toordinal())
		labels.append(d.strftime('%x'))

	min = db.read_minimums(times)
	avg = db.read_averages(times)
	max = db.read_maximums(times)
	
	response = json.dumps( {'min': min, 'avg':avg, 'max':max, 'day':labels}) 
	return response

