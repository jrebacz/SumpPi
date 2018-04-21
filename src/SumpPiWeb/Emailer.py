import smtplib
from SumpPiWeb import config

class Emailer(object):
		"""Sends e-mail using SMTP"""

		def __init__(self):
			self.recipients = config.MAILING_LIST

		def mail(self):
			if not config.MAILING_USER or not config.MAILING_PASSWORD:
				return

			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(config.MAILING_USER, config.MAILING_PASSWORD)

			for recipient in self.recipients:
				msg = "To: " + recipient + "\r\n" + "From: "+ config.MAILING_USER + """
Subject: Sump water level alarm
High water level detected in the sump pit!
Monitor water level here http://sumppi:5555"""
				server.sendmail(config.MAILING_USER, recipient, msg)
			server.quit()
