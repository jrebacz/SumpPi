"""
The flask application package.
"""

from flask import Flask
from flask_basicauth import BasicAuth
from SumpPiWeb import config
app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = config.PUBLISHER_USER
app.config['BASIC_AUTH_PASSWORD'] = config.PUBLISHER_PASSWORD
basic_auth = BasicAuth(app)

import SumpPiWeb.views
import SumpPiWeb.controllers
import SumpPiWeb.cloud_controllers
import SumpPiWeb.config