
import datetime
import time
import os
import ZODB
import ZODB.FileStorage
import ZODB.DB

import BTrees
import persistent
import transaction

class Database:
	def __init__(self):
		try:
			self.storage = ZODB.FileStorage.FileStorage('database.fs')
			self.db = ZODB.DB(self.storage)
			self.connection = self.db.open()
			self.root = self.connection.root()
		except:
			print("Exception occurred initializing database")
			pass

		def __del__(self):
			connection.close()

		# Create Trees if they don't exist
		for attribute in ['minimums', 'maximums', 'averages']:
			if not hasattr(self.root, attribute):
				setattr(self.root, attribute, BTrees.LOBTree.BTree())
		
		self.minimums = self.root.minimums
		self.maximums = self.root.maximums
		self.averages = self.root.averages

		if not hasattr(self.root, 'alarm_settings'):
			setattr(self.root, 'alarm_settings', BTrees.OOBTree.BTree())
			self.alarm_settings = self.root.alarm_settings
			#assign defaults
			self.store_alarm_distance(-12.0)
			self.store_alarm_time_in_alarm(5.0)
			self.store_alarm_enable_audible_alarm('true')
		self.alarm_settings = self.root.alarm_settings

	def store_summary(self, _min, _max, _avg, _t):
		self.minimums[_t] = _min
		self.maximums[_t] = _max
		self.averages[_t] = _avg
		transaction.commit()

	def read_keys(self, attrib, _times):
		result = []
		for t in _times:
			if getattr(self, attrib).has_key(t):
				result.append(getattr(self, attrib)[t])
			else:
				result.append(None)
		return result
	
	def read_minimums(self, _times):
		return self.read_keys('minimums', _times)
	
	def read_maximums(self, _times):
		return self.read_keys('maximums', _times)
	
	def read_averages(self, _times):
		return self.read_keys('averages', _times)

	# Alarm configuration
	def store_alarm_distance(self, _distance):
		if _distance > 0.0:
			_distance = -_distance
		self.alarm_settings['distance'] = _distance
		transaction.commit()

	def read_alarm_distance(self):
		return self.alarm_settings['distance']

	def store_alarm_time_in_alarm(self, _time_in_alarm):
		self.alarm_settings['time_in_alarm'] = _time_in_alarm
		transaction.commit()

	def read_alarm_time_in_alarm(self):
		return self.alarm_settings['time_in_alarm']

	def store_alarm_enable_audible_alarm(self, _enable_audible_alarm):
		self.alarm_settings['enable_audible_alarm'] = _enable_audible_alarm
		transaction.commit()

	def read_alarm_enable_audible_alarm(self):
		return self.alarm_settings['enable_audible_alarm']
