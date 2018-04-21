from datetime import datetime


class DailySummaryReturn:
	def __init__(self, has_summary, day_ordinal=0, min_max_avg=[]):
		self.has_summary = has_summary
		self.day_ordinal = day_ordinal
		self.min_max_avg = min_max_avg

class DailySummaryCalculator(object):
	"""Calculates the previous days statistics"""

	def __init__(self):
		self.last_day = 0

	def calculate(self, series):
		if len(series) == 1:
			self.last_day = datetime.fromtimestamp(series[0].utc).toordinal()
			return DailySummaryReturn(False)

		j = len(series) - 1
		i = j

		day = datetime.fromtimestamp(series[j].utc).toordinal()

		if self.last_day == day:
			return DailySummaryReturn(False)

		# Find the range of days to calculate over
		while i > 0 and datetime.fromtimestamp(series[i - 1].utc).toordinal() == self.last_day:
			i-=1
		if i == j:
			self.last_day = day
			return DailySummaryReturn(False)
		
		last_min = series[i].y
		last_max = series[i].y
		running_sum = 0

		for m in series[i:j]:
			last_min = min(last_min, m.y)
			last_max = max(last_max, m.y)
			running_sum += m.y

		ret = DailySummaryReturn(True, self.last_day, [last_min, last_max, running_sum/(j-i)])
		self.last_day = day
		return ret