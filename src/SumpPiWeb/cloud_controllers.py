import datetime


import threading
import _thread
import time
import datetime
import json

from SumpPiWeb import basic_auth
from SumpPiWeb.controllers import db

from flask import request
from SumpPiWeb import app
from SumpPiWeb import views
from SumpPiWeb.Measurement import Measurement
from SumpPiWeb.DistanceReader import DistanceReader
from SumpPiWeb import controllers


@app.route('/depth', methods=['PUT'])
@basic_auth.required
def put_depth():
	distance = float(request.json['y'])
	controllers.dist_rdr.add_reading(distance)
	return 'success'

@app.route('/alarm_settings/distance', methods=['POST'])
@basic_auth.required
def set_alarming_alarm_settings_distance():
	db.store_alarm_distance(float(request.json['distance']))
	return 'success'