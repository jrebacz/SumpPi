# SumpPi
A sump pit monitoring service using Python Flask on a Raspberry Pi

The Pi measures the distance from the top of the sump pit to the water surface with an acoustic sensor.  Once the water level raises above a threshold, emails and SMS alerts send out, and an audible alarm sounds.  The Python Flask app provides a web interface for real-time and historical viewing of the water level.  The Pi can be configured to publish to another instance of the same Python Flask app on the cloud.

![alt text](https://github.com/jrebacz/SumpPi/blob/master/doc/images/system_diagram.png "system diagram")

The first working prototype is shown below.  The breadboard circuitry is needed for interfacing the Raspberry Pi's GPIO pins with the acoustic sensor, and for switching on a 9V circuit for sounding a piezo buzzer (a tuned 555 timer provides the piezo buzzer with the resonance frequency needed to hear the alarm through the floor)

![alt text](https://github.com/jrebacz/SumpPi/blob/master/doc/images/prototype.jpg "prototype")
