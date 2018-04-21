import time
from threading import Thread

import threading
import datetime
import random

from SumpPiWeb import Alarm, Emailer,config, cloud_request
from SumpPiWeb.Measurement import Measurement
from SumpPiWeb.DailySummaryCalculator import DailySummaryCalculator

is_gpio_imported = True
TRIG = 23
ECHO = 24
try:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)
except ImportError:
	is_gpio_imported = False

class DistanceReader(Thread):
	"""description of class"""

	def __init__(self, db):
		Thread.__init__(self)
		self.db = db
		
		self.dsc = DailySummaryCalculator()
		self.alarm_system = Alarm.Alarm()
		self.alarm_system.audible_alarm_enabled = db.read_alarm_enable_audible_alarm() == 'true'

		self.thread_lock = threading.Lock()
		self.depth_series = []
		self.end_thread = False

		self.emailer = Emailer.Emailer()
		self.last_email_time = 0
		
	def run(self):
		if config.CLOUD:
			return

		self.alarm_system.start()
		while not self.end_thread:
			time.sleep(config.POLL_PERIOD)
			if is_gpio_imported:
				depth = self.get_distance_median(config.POLL_SAMPLES)
				cloud_request.SendMeasurementToCloud(depth)
				self.add_reading(depth)
			else:
				depth = random.random()*10.0
				cloud_request.SendMeasurementToCloud(depth)
				self.add_reading(depth)
		self.alarm_system.end_thread = True
		self.alarm_system.join()
		if is_gpio_imported:
			GPIO.cleanup()
			print("GPIO cleanup has been called")

	def get_distance(self):

		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		timeout = time.time()
		while GPIO.input(ECHO)==0:
				pulse_start = time.time()
				if pulse_start > timeout + 1.0:
					raise Exception("Bad reading: missed 0")
				
		while GPIO.input(ECHO) == 1:
				pulse_end = time.time()
				if pulse_end > timeout + 1.0:
					raise Exception("Bad reading: missed 1")
				
		pulse_duration = pulse_end - pulse_start
		distance = round(pulse_duration*17150, 2)
		return distance

	def get_distance_median(self, samples):
		GPIO.output(TRIG, False)
		time.sleep(0.2)

		results = []
		while len(results) < samples:
			try:
				results.append(self.get_distance())
			except Exception as error:
				print(repr(error))
		results.sort()
		print("Distances: " + str(results))
		return results[int(samples/2)]
	
	def add_reading(self, depth):
		depth = -depth;

		now = datetime.datetime.now().replace(microsecond=0)
		self.thread_lock.acquire()		
		self.depth_series.append( Measurement(depth, now.timestamp()))
		self.thread_lock.release()
		self.alarm_system.check_alarm_condition(self.depth_series, self.db.read_alarm_distance(), self.db.read_alarm_time_in_alarm())
	
		#Email alerts at most 1 per hour
		if not config.CLOUD and self.alarm_system.sound_alarm and time.time() > self.last_email_time + 3600:
			self.last_email_time = time.time()
			print("Sending out an email alert")
			self.emailer.mail()

		ret = self.dsc.calculate(self.depth_series)
		if ret.has_summary:
			self.db.store_summary(ret.min_max_avg[0], ret.min_max_avg[1], ret.min_max_avg[2], ret.day_ordinal)
		
