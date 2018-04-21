# SumpPi
A sump pit monitoring service using Python Flask on a Raspberry Pi

The Pi measures the distance from the top of the sump pit to the water surface with an acoustic sensor.  Once the water level raises above a threshold, emails and SMS alerts send out, and an audible alarm sounds.  The Python Flask app provides a web interface for real-time and historical viewing of the water level.  The Pi can be configured to publish to another instance of the same Python Flask app on the cloud.
