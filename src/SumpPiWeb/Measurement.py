import json
import datetime

class Measurement:
	def __init__(self, y, utc):
		self.y = y
		self.utc = utc
		self.t = datetime.datetime.fromtimestamp(utc).strftime('%b %d %H:%M:%S')


class CustomEncoder(json.JSONEncoder):

	def default(self, o):
		if isinstance(o, Measurement):
			return {'x': o.utc, "y": o.y}
		return {'__{}__'.format(o.__class__.__name__): o.__dict__}