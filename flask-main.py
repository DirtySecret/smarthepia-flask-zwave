#! /usr/bin/env python

import sys
import time
import logging
import configpi
import os

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response
from backend import Backend

app = Flask(__name__)

backend = Backend()

@app.route('/')
def index():
    return render_template("index.html", title=configpi.name)
	
#######################################################################################################################
############# NETWORK #################################################################################################
#######################################################################################################################
	
@app.route('/network/preview')
def network_preview():
    return backend.network_preview()

@app.route('/network/debug')
def network_debug():
    return backend.network_debug()

@app.route('/network/timestamps')
def network_timestamp():
    return backend.network_timestamp()	

@app.route('/network/configureNodes')
def network_configureNodes():
    return backend.set_sensor()   ################## a revoir
	
@app.route('/network/nodesConfiguration')
def network_nodesConfiguration():
    return backend.network_nodesConfiguration()  ######## a revoir
    
@app.route('/network/restart')
def restart():
    backend.stop()
    time.sleep(3)
    backend.start()
    return "Z-Wave Network Restarted"

@app.route('/network/start')
def start():
    backend.start()
    return "Z-Wave Network Started"

@app.route('/network/stop')
def stop():
    backend.stop()
    time.sleep(2)
    return "Z-Wave Network Stopped"

@app.route('/network/updateRoutes')
def network_updateRoutes():
    return backend.healNetwork(True)
	
@app.route('/network/updateNeighbourhood')
def network_updateNeighbourhood():
    return backend.healNetwork()

#######################################################################################################################
############# SENSORS #################################################################################################
#######################################################################################################################

@app.route('/sensors')
def sensors():
	return Response(backend.get_sensors, mimetype="text/plain")

@app.route('/sensors/add')
def add_device():
    return backend.addDevice()

@app.route('/sensors/remove')
def remove_device():
    return backend.removeDevice()
	
@app.route('/sensors/<node>/all_measures')
def get_all_measures(node):
    return backend.allMeasures(node)

@app.route('/sensors/<node>/temperature')
def get_temperature(node):
    return backend.temperature(node)

@app.route('/sensors/<node>/humidity')
def get_humidity(node):
    return backend.humidity(node)

@app.route('/sensors/<node>/luminance')
def get_luminance(node):
    return backend.luminance(node)

@app.route('/sensors/<node>/motion')
def get_motion(node):
    return backend.motion(node)
    
@app.route('/sensors/<node>/updateRoutes')
def node_updateRoutes(node):
    return backend.healNode(node, True)

@app.route('/sensors/<node>/updateNeighbourhood')
def node_updateNeighbourhood(node):
    return backend.healNode(node)

@app.route('/sensors/<node>/refresh')
def refreshNode(node):
    return backend.refreshNode(node)

@app.route('/sensors/<node>/set/<int:param>/to/<int:value>')
def set_config_param(node, param, value):
    return backend.set_node_config_param(node, param, value)

@app.route('/sensors/<node>/get/<int:param>')
def get_config_param(node, param):
    return backend.get_node_config_param(node, param)

########################################################################################################################
############# SWITCHES #################################################################################################
########################################################################################################################

@app.route('/switches')
def switches():
	return Response(backend.get_switches, mimetype="text/plain")

@app.route('/switches/<node>/<on_off_check>')
def switch(node, on_off_check):
    if on_off_check == 'on':
        backend.switch_on(node)
        return "switch %s switched on" % node
    elif on_off_check == 'off':
        backend.switch_off(node)
        return "switch %s switched off" % node
    elif on_off_check == 'check':
        val = backend.get_switch_status(node)
        if val:
            return "switch %s is currently on" % node
        else:
            return "switch %s is currently off" % node
    elif on_off_check == 'on1':
        backend.switch_on1(node)
        return "switch %s switched on" % node
    elif on_off_check == 'off1':
        backend.switch_off1(node)
        return "switch %s switched on" % node
    elif on_off_check == 'check1':
        val = backend.get_switch_status1(node)
        if val:
            return "switch %s is currently on" % node
        else:
            return "switch %s is currently off" % node
    elif on_off_check == 'on2':
        backend.switch_on2(node)
        return "switch %s switched on" % node
    elif on_off_check == 'off2':
        backend.switch_off2(node)
        return "switch %s switched off" % node
    elif on_off_check == 'check2':
        val = backend.get_switch_status2(node)
        if val:
            return "switch %s is currently on" % node
        else:
            return "switch %s is currently off" % node
    else:
        return "unrecognised command - choose on/off/check"
		

		
		
########################################################################################################################
############# DEVICES ##################################################################################################
########################################################################################################################		
		
		
@app.route('/devices')
def devices():
    devices = backend.get_devices()
    if type(devices) is str:
	return devices
    devices_list = ""
    for key, val in devices.items():
	    devices_list += str(key) + "=" + str(val) + "\n"
    return Response(devices_list, mimetype="text/plain")
    #return render_template("index.html")

@app.route('/devices/<node>/setLocationTo/<str:value>')
def set_node_location(node, value):
    return backend.set_node_location(node, value)

@app.route('/devices/<node>/setNameTo/<str:value>')
def set_node_name(node, value):
    return backend.set_node_name(node, value)
	
################################################
"""@app.route('/network/refresh')	
def refreshNetworkInfo():
    return backend.refreshNodes()
"""
########### CONTROLLER ################
''' Find a way to secure this route (login form, security code, etc.)
@app.route('/controller/reset')
def hardReset():
    return backend.reset()
'''
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

	
## LOGGING TEST
#@app.route('/logtest')
#def log():
#    return 1/0

#################################################################
#################################################################	

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