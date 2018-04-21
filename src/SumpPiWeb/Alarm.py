from sys    import stdout
from time   import sleep
from threading import Thread

ALARM = 18
is_gpio_imported = True
try:
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ALARM, GPIO.OUT)
except ImportError:
	is_gpio_imported = False

class Alarm(Thread):
		"""Detects alarm condition"""

		def __init__(self):
			Thread.__init__(self)
			self.sound_alarm = False
			self.end_thread = False
			self.audible_alarm_enabled = True
		
		def run(self):
			while not self.end_thread:
				if self.sound_alarm and self.audible_alarm_enabled:
					self.sound_the_alarm()
					sleep(0.25)
				else:
					sleep(1.0)

		def sound_the_alarm(self):
			if is_gpio_imported:
				if self.audible_alarm_enabled:
					for i in range(4):
						GPIO.output(ALARM, True)
						sleep(0.1 * i)
						GPIO.output(ALARM, False)
						sleep(0.1)
	
					GPIO.output(ALARM, True)
					sleep(.5)
					GPIO.output(ALARM, False) 
	
					GPIO.output(ALARM, False)
				else:
					print("Audible alarm is muted")
			else:
				print("beep")


		def check_alarm_condition(self, series, distance, time_in_alarm):
			val = len(series)-1

			if val < 2:
				self.sound_alarm = False
				return False
			
			# The last values must be less than the alarm distance
			latest_time = series[val].utc
			while(val > 0 and series[val].y >= distance):
				# An alarm occurs the last values have been less than the alarm distance for 'time_in_alarm' seconds
				if latest_time >= series[val].utc + time_in_alarm:
					self.sound_alarm = True
					return True
				val-=1
			self.sound_alarm = False
			return False

