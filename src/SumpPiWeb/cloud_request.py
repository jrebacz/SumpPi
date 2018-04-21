import requests
from SumpPiWeb import config

def RequestToCloud(method, url, data, ):
	headers = {"Content-Type":"application/json"}
	try:
		response = requests.request(method, url, data=data, headers=headers, timeout=4.0, auth=(config.PUBLISHER_USER,config.PUBLISHER_PASSWORD), verify=False)
	except requests.exceptions.ConnectionError:
		print("Error connecting to cloud.")
	except requests.exceptions.Timeout:
		print("Request to cloud timed out.")
	except requests.exceptions.RequestException:
		print("Request exception.")

def SendMeasurementToCloud(y):
	if not config.PUBLISHER_ENDPOINT:
		return
	url = config.PUBLISHER_ENDPOINT	 + '/depth'
	data = '{"y": "' + str(y)+'"}'
	RequestToCloud('PUT', url, data)

def SendAlarmDistanceToCloud(distance):
	if not config.PUBLISHER_ENDPOINT:
		return
	url = config.PUBLISHER_ENDPOINT	+ '/alarm_settings/distance'
	data = '{"distance": "' + str(distance)+'"}'
	RequestToCloud('POST', url, data)
	