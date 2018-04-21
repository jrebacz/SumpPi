import unittest
from time import mktime
from DailySummaryCalculator import *
from Measurement import Measurement

class TestCalculation(unittest.TestCase):
	def test_one_val(self):		
		dsc = DailySummaryCalculator()
		ret = dsc.calculate([Measurement(1.2, 1519862400)])
		self.assertFalse(ret.has_summary)

	def test_one_day(self):
		dsc = DailySummaryCalculator()

		series = [Measurement(1.2, mktime(datetime(2018,3,1, 0, 0, 0).timetuple())) ]

		ret = dsc.calculate(series)

		series.append(Measurement(1.3, mktime(datetime(2018,3,1, 1, 0, 0).timetuple())))

		ret = dsc.calculate(series)
		self.assertFalse(ret.has_summary)

		series.append(Measurement(1.7, mktime(datetime(2018,3,1, 23, 0, 0).timetuple())))
		ret = dsc.calculate(series)
		self.assertFalse(ret.has_summary)

		series.append(Measurement(1.8, mktime(datetime(2018,3,1, 23, 59, 59).timetuple())))

		ret = dsc.calculate(series)
		self.assertFalse(ret.has_summary)

		#trigger a calculation
		series.append(Measurement(999, mktime(datetime(2018,3,2, 0, 0, 0).timetuple())))
		ret = dsc.calculate(series)
		self.assertTrue(ret.has_summary)

		self.assertEqual(1.2, ret.min_max_avg[0])
		self.assertEqual(1.8, ret.min_max_avg[1])
		self.assertEqual(1.5, ret.min_max_avg[2])

	def test_week(self):
		series = []
		dsc = DailySummaryCalculator()
		ret = []
		for i in range(1,7):
			v = i
			t = mktime(datetime(2018,3,i, 0, 0, 0).timetuple())
			series.append(Measurement(v,t))
			ret.append(dsc.calculate(series))
		for r in ret[2:6]:
			self.assertTrue(r.has_summary)

		for i in range(1,6):
			self.assertEqual(i, ret[i].min_max_avg[0])
			self.assertEqual(i, ret[i].min_max_avg[1])
			self.assertEqual(i, ret[i].min_max_avg[2])

	def test_calculations(self):
		series = []
		dsc = DailySummaryCalculator()
		ret = []

		input_24_values = [11.5,3.56,6.78,5.35,7.86,5.44,7.85,45.67,34.67,3.7,8.9,3.6,8.4,7.8,4.2,5.6,7.4,9.0,6.4,2.3,6.78,98.56,3.56,8.6]
		series.append(Measurement(1.0, mktime(datetime(2018,3,1, 1, 0, 0).timetuple())))
		dsc.calculate(series)
		for i in range(0,24):
			series.append(Measurement(input_24_values[i], mktime(datetime(2018,3,2, i, 0, 0).timetuple()) ))
			dsc.calculate(series)
		series.append(Measurement(1.0, mktime(datetime(2018,3,3, 0, 0, 0).timetuple())))
		ret = dsc.calculate(series)
		
		expected_min = min(input_24_values)
		expected_max = max(input_24_values)
		expected_avg = sum(input_24_values) / len(input_24_values)

		self.assertEquals(expected_min, ret.min_max_avg[0])
		self.assertEquals(expected_max, ret.min_max_avg[1])
		self.assertEquals(expected_avg, ret.min_max_avg[2])


if __name__ == '__main__':
	unittest.main()