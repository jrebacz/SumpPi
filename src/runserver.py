"""
This script runs the SumpPiWeb application using a development server.
"""

from os import environ
from SumpPiWeb import app
from SumpPiWeb.controllers import end_threads
from flask import session
from SumpPiWeb import views, config


if __name__ == '__main__':
	app.run(config.SERVER_HOST, config.SERVER_PORT, debug = True, use_reloader=False)
	print("Ending threads . . .")
	end_threads()
	print("Successfully shut down")