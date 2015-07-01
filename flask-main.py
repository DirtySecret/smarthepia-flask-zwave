#! /usr/bin/env python

import sys
import os
import logging
import time

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response
from backend import Backend

app = Flask(__name__)

backend = Backend()

API_DESCRIPTION = """<h1>API DESCRIPTION</h1>
	<h2>Network Routes</h2>
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
		<td><b>/network/info</b></td>
		<td>Return some debug values about the network and all the values contained in nodes</td>
	</tr>
        <tr style="border: 1px solid black;">
		<td><b>/network/configure</b><br/>
		<td>Send config values to every awake nodes (e.g.: Interval in seconds to report Sensors Values)</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/network/configuration</b><br/>
                <td>List the config values in every awake nodes (e.g.: Interval in seconds to report Sensors Values)</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/network/restart</b><br/>
                <td>Restart Z-Wave Network</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/network/start</b><br/>
                <td>Start the Z-Wave Network</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/network/stop</b><br/>
                <td>Stop the Z-Wave Network</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/network/healWithRoutes</b></td>
                <td>Heal network by asking nodes to rediscover their neighbours + Init new routes</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/network/healOnly</b></td>
                <td>Heal network by asking nodes to rediscover their neighbours</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/network/refresh</b></td>
                <td>Refresh the informations held by nodes in the network (config & sensor values)</td>
        </tr>
        </table>
        
        <h2>Controller Routes</h2>
        <table style="width: 100%; margin: auto; border-collapse:collapse; border: 1px solid black;">
        <tr style="background-color: black; color: white; font-size: x-large;">
                <th style="witdh: 40%;">Routes</th>
                <th style="witdh: 60%;">Description</th>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/controller/reset</b></td>
                <td>Hard reset the controller and clear sensor indexes (exclude any sensors before reseting the controller)</td>
        </tr>
        </table>
        
        <h2>Sensors Routes</h2>
        <table style="width: 100%; margin: auto; border-collapse:collapse; border: 1px solid black;">
        <tr style="background-color: black; color: white; font-size: x-large;">
                <th style="witdh: 40%;">Routes</th>
                <th style="witdh: 60%;">Description</th>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/sensors/{$sensor_id}/healWithRoutes</b></td>
                <td>Heal sensor $sensor_id by rediscovering its neighbours + Init new routes</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/sensors/{$sensor_id}/healOnly</b></td>
                <td>Heal sensor $sensor_id by rediscovering its neighbours</td>
        </tr>
        <tr style="border: 1px solid black;">
                <td><b>/sensor/{$sensor_id}/refresh</b></td>
                <td>Refresh node info for sensor $sensor_id</td>
        </tr>
        <tr style="border: 1px solid black;">
		<td><b>/sensor/{$sensor_id}/get_all</b></td>
		<td>Return all measures (temp, hum, lum, motion) for sensor $sensor_id</td>
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
	<tr style="border: 1px solid black;">   
                <td><b>/sensor/add</b></td>
                <td>Add a device when its add button is pressed</td>
        </tr>
        <tr style="border: 1px solid black;">   
                <td><b>/sensor/remove</b></td>
                <td>Remove a device when its button is pressed</td>
        </tr>
        <tr style="border: 1px solid black;">   
                <td><b>/sensor/{$sensor_id}/set/{$param_index}/to/{$param_value}</b></td>
                <td>Set $param_value as value for the parameter $param_index</td>
        </tr>
        <tr style="border: 1px solid black;">   
                <td><b>/sensor/{$sensor_id}/get/{$param_index}</b></td>
                <td>Get the value for the parameter $param_index</td>
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
        <b>value</b> : Value of the sensor, possible types : <i>float</i> for temperature(deg. celsius), humidity(%age) and luminosity(lux) ; <i>boolea$
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

@app.route('/network/info')
def networkinfo():
    return backend.network_info()

@app.route('/network/timestamps')
def networktimestamp():
    return backend.network_timestamp()
    
@app.route('/network/restart')
def restart():
    backend.stop()
    time.sleep(5)
    backend.start()
    return "Z-Wave Network Restarted"

@app.route('/network/start')
def start():
    backend.start()
    return "Z-Wave Network Started"

@app.route('/network/stop')
def stop():
    backend.stop()
    time.sleep(5)
    return "Z-Wave Network Stopped"

@app.route('/network/healOnly')
def healNetworkOnly():
    return backend.healNetwork()

@app.route('/network/healWithRoutes')
def healNetworkAndRoutes():
    return backend.healNetwork(True)
    
@app.route('/network/configuration')
def networkConfiguration():
    return backend.networkConfiguration()

@app.route('/network/refresh')	
def refreshNetworkInfo():
    return backend.refreshNodes()
    


########### CONTROLLER ################

@app.route('/controller/reset')
def hardReset():
    return backend.reset()

    
    
############# SENSORS #################    
    
@app.route('/sensor/<node>/healOnly')
def healNodeOnly(node):
    return backend.healNode(node)

@app.route('/sensor/<node>/healWithRoutes')
def healNodeAndRoutes(node):
    return backend.healNode(node, True)

@app.route('/sensor/<node>/refresh')
def refreshNode(node):
    return backend.refreshNode(node)

@app.route('/sensor/<node>/set/<int:param>/to/<int:value>')
def set_config_param(node, param, value):
    return backend.set_node_config_param(node, param, value)

@app.route('/sensor/<node>/set/<int:param>')
def get_config_param(node, param):
    return backend.get_node_config_param(node, param)

@app.route('/sensor/add')
def add_device():
    return backend.addDevice()

@app.route('/sensor/remove')
def remove_device():
    return backend.removeDevice()

@app.route('/sensor/<node>/get_all')
def get_all_measures(node):
    return backend.allMeasures(node)

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

@app.route('/network/configure')
def configuration():
    return backend.set_sensor()

@app.route('/logtest')
def log():
    return 1/0

@app.route('/switch/<node>/<on_off_check>')
def switch(node, on_off_check):
    if on_off_check == 'on':
        backend.switch_on(node)
        return "switch %s switched on" % node
    elif on_off_check == 'off':
        backend.switch_off(node)
        return "switch %s switched on" % node
    elif on_off_check == 'check':
        val = backend.get_switch_status(node)
        if val:
            return "switch %s is currently on" % node
        else:
            return "switch %s is currently off" % node
    else:
        return "unrecognised command - choose on/off/check"

from logging import FileHandler, Formatter, DEBUG

if __name__ == '__main__':
    try:
        backend.start()
    	file_handler = FileHandler("flask.log")
    	file_handler.setLevel(DEBUG)
    	file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    	app.logger.addHandler(file_handler)

        app.run(host='::', debug=False, use_reloader=False)

        #app.run(host='2001:620:607:5e16::314', debug=True, use_reloader=False)
        #app.run(host='pi1.smarthepia.distantaccess.com', debug=True, use_reloader=False)
    except KeyboardInterrupt:
        backend.stop()
