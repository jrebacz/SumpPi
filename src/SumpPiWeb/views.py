"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from SumpPiWeb import app, config

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
				cloud=config.CLOUD
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/historical')
def historical():
    """Renders the historical page."""
    return render_template(
        'historical.html',
        title='Historical',
        year=datetime.now().year,
        message='Displays past daily statistics.'
    )
