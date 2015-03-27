#! /usr/bin/env python

import sys
import os
import logging
file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response
from backend import Backend

app = Flask(__name__)

backend = Backend()

API_DESCRIPTION = """<h1>API DESCRIPTION</h1>
	<table style="width: 100%; margin: auto; border-collapse:collapse; border: 1px solid black;">
	<tr style="background-color: black; color: white; font-size: x-large;">
		<th style="witdh: 40%;">Routes</th>
		<th style="witdh: 60%;">Description</th>
	</tr>
	<tr style="border: 1px solid black;">
		<td><b>/list</b></td>
		<td>List all sensors paired with this controller</td>
	</tr>
	<tr style="border: 1px solid black;">
		<td><b>/rglist</b></td>
		<td>Modern list of all sensors paired with this controller, with more info available</td>
	</tr>
	<tr style="border: 1px solid black;">
		<td><b>/networkinfo</b></td>
		<td>Return some debug values about the network and all the values contained in nodes</td>
	</tr>
        <tr style="border: 1px solid black;">
		<td><b>/configuration</b><br/>
		<td>Send config values to every awake nodes (e.g.: Interval in seconds to report Sensors Values)</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/restart</b><br/>
        	<td>Restart Z-Wave Network</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/start</b><br/>
        	<td>Start the Z-Wave Network</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/stop</b><br/>
        	<td>Stop the Z-Wave Network</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/healNetworkAndRoutes</b></td>
		<td>Heal network by asking nodes to rediscover their neighbours + Init new routes</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/healNetworkOnly</b></td>
		<td>Heal network by asking nodes to rediscover their neighbours</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/healNodeAndRoutes/{$sensor_id}</b></td>
		<td>Heal sensor $sensor_id by rediscovering its neighbours + Init new routes</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/healNodeOnly/{$sensor_id}</b></td>
		<td>Heal sensor $sensor_id by rediscovering its neighbours</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/refreshNetworkInfo</b></td>
		<td>Refresh the informations held by nodes in the network (config & sensor values)</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/sensor/{$sensor_id}/get_temperature</b></td>
		<td>Return current temperature for sensor $sensor_id</td>
        </tr>
        <tr style="border: 1px solid black;">	
		<td><b>/sensor/{$sensor_id}/get_humidity</b></td>
		<td>Return current humidity for sensor $sensor_id</td>
        </tr>
        <tr style="border: 1px solid black;">		
		<td><b>/sensor/{$sensor_id}/get_luminance</b></td>
		<td>Return current luminance for sensor $sensor_id</td>
	</tr>
	<tr style="border: 1px solid black;">	
		<td><b>/sensor/{$sensor_id}/get_motion</b></td>
		<td>Return presence detection value for sensor $sensor_id</td>
	</tr>
	</table>
	<br/><br/>
	JSON format :<br/>
	<span style="font-family:'Courier New';font-size:13">{<br/>
	&nbsp;&nbsp;"controller": CONTROLLER_NAME,<br/>
        &nbsp;&nbsp;"location": SENSOR_LOCATION, <br/>
	&nbsp;&nbsp;"sensor": SENSOR_ID,<br/>
	&nbsp;&nbsp;"type": SENSOR_TYPE, <br/>
	&nbsp;&nbsp;"updateTime": TIMESTAMP,<br/> 
	&nbsp;&nbsp;"value": SENSOR_VALUE<br/>
	}<br/><br/></span>
	
	Fields description :<br/>
	<span style="font-family:'Courier New';font-size:13">
	<b>controller</b> : String desribing the controller (Raspberry name)<br/>
	<b>location</b> : Precise location of the sensor in his network<br/>
	<b>sensor</b> : Value describing the sensor (integer value)<br/>
	<b>type</b> : String describing the sensor, possible values : <i>"temperature", "humidity", "presence", "luminosity"</i><br/>
	<b>updateTime</b> : Timestamp of last update <br/>
	<b>value</b> : Value of the sensor, possible types : <i>float</i> for temperature(deg. celsius), humidity(%age) and luminosity(lux) ; <i>boolean</i> for presence<br/>
	</span>
"""

@app.route('/')
def index():
    return API_DESCRIPTION

@app.route('/list')
def devices_list():
    devices = backend.get_devices()
    if type(devices) is str:
	return devices
    devices_list = ""
    for key, val in devices.items():
	    devices_list += str(key) + "=" + str(val) + "\n"
    return Response(devices_list, mimetype="text/plain")
    #return render_template("index.html")
    
@app.route('/rglist')
def rglist():
    return backend.rgList()

@app.route('/networkinfo')
def networkinfo():
    return backend.network_info()
    
@app.route('/restart')
def restart():
    backend.stop()
    time.sleep(5)
    backend.start()
    return "Z-Wave Network Restarted"

@app.route('/start')
def start():
    backend.start()
    return "Z-Wave Network Started"

@app.route('/stop')
def stop():
    backend.stop()
    time.sleep(5)
    return "Z-Wave Network Stopped"

@app.route('/healNetworkAndRoutes')
def healNetworkAndRoutes():
    return backend.healNetwork(True)
    
@app.route('/healNetworkOnly')
def healNetworkOnly():
    return backend.healNetwork()
    
@app.route('/healNodeAndRoutes/<node>')
def healNodeAndRoutes(node):
    return backend.healNode(node, True)
    
@app.route('/healNodeOnly/<node>')
def healNodeOnly(node):
    return backend.healNode(node)

@app.route('/refreshNetworkInfo')	
def refreshNetworkInfo():
    return backend.refreshNodes()

@app.route('/sensor/<node>/get_temperature')
def get_temperature(node):
    return backend.temperature(node)

@app.route('/sensor/<node>/get_humidity')
def get_humidity(node):
    return backend.humidity(node)

@app.route('/sensor/<node>/get_luminance')
def get_luminance(node):
    return backend.luminance(node)

@app.route('/sensor/<node>/get_motion')
def get_motion(node):
    return backend.motion(node)

@app.route('/rgtest')
def rgtest():
    return backend.rgtest_method()

#@app.route('/updateNeighbours/<node>')
#def upN(node):
#    return backend.updateNeighboursList(node)


    
# OLD METHODS    

@app.route('/temperature/<node>')
def temperature(node):
    return backend.get_temperature(node)

@app.route('/humidity/<node>')
def humidity(node):
    return backend.get_humidity(node)

@app.route('/luminance/<node>')
def luminance(node):
    return backend.get_brightness(node)

@app.route('/motion/<node>')
def motion(node):
    return backend.get_motion(node)

# CONFIGURATION

@app.route('/configuration')
def configuration():
    return backend.set_sensor()

@app.route('/logtest')
def log():
    return 1/0

from logging import FileHandler, Formatter

if __name__ == '__main__':
    try:
        backend.start()
    	file_handler = FileHandler("flask.log")
    	file_handler.setLevel(logging.DEBUG)
    	file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    	app.logger.addHandler(file_handler)

        app.run(host='::', debug=False, use_reloader=False)

        #app.run(host='2001:620:607:5e16::314', debug=True, use_reloader=False)
        #app.run(host='pi1.smarthepia.distantaccess.com', debug=True, use_reloader=False)
    except KeyboardInterrupt:
        backend.stop()
