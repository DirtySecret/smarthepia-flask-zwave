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

@app.route('/', strict_slashes=False)
def index():
    return render_template("index.html", title=configpi.name)
    
#######################################################################################################################
############# NETWORK #################################################################################################
#######################################################################################################################
    
@app.route('/network/preview', strict_slashes=False)
def network_preview():
    return backend.network_preview()

@app.route('/network/debug', strict_slashes=False)
def network_debug():
    return backend.network_debug()

@app.route('/network/timestamps', strict_slashes=False)
def network_timestamp():
    return backend.network_timestamp()    

@app.route('/network/configureNodes', strict_slashes=False)
def network_configureNodes():
    return backend.set_sensor()   ################## a revoir
    
@app.route('/network/nodesConfiguration', strict_slashes=False)
def network_nodesConfiguration():
    return backend.network_nodesConfiguration()  ######## a revoir
    
@app.route('/network/restart', strict_slashes=False)
def restart():
    backend.stop()
    time.sleep(3)
    backend.start()
    return "Z-Wave Network Restarted"

@app.route('/network/start', strict_slashes=False)
def start():
    backend.start()
    return "Z-Wave Network Started"

@app.route('/network/stop', strict_slashes=False)
def stop():
    backend.stop()
    time.sleep(2)
    return "Z-Wave Network Stopped"

@app.route('/network/updateRoutes', strict_slashes=False)
def network_updateRoutes():
    return backend.healNetwork(True)
    
@app.route('/network/updateNeighbourhood', strict_slashes=False)
def network_updateNeighbourhood():
    return backend.healNetwork()

#######################################################################################################################
############# SENSORS #################################################################################################
#######################################################################################################################

@app.route('/sensors', strict_slashes=False)
def sensors():
    sensors = backend.get_sensors()
    if type(sensors) is str:
        return sensors
    sensors_list = ""
    for key, val in sensors.items():
        sensors_list += str(key) + "=" + str(val) + "\n"
    return Response(sensors_list, mimetype="text/plain")
    
@app.route('/sensors/<int:node>/all_measures', strict_slashes=False)
def get_all_measures(node):
    return backend.allMeasures(node)

@app.route('/sensors/<int:node>/temperature', strict_slashes=False)
def get_temperature(node):
    return backend.temperature(node)

@app.route('/sensors/<int:node>/humidity', strict_slashes=False)
def get_humidity(node):
    return backend.humidity(node)

@app.route('/sensors/<int:node>/luminance', strict_slashes=False)
def get_luminance(node):
    return backend.luminance(node)

@app.route('/sensors/<int:node>/motion', strict_slashes=False)
def get_motion(node):
    return backend.motion(node)

@app.route('/sensors/<int:node>/updateRoutes', strict_slashes=False)
def node_updateRoutes(node):
    return backend.healNode(node, True)

@app.route('/sensors/<int:node>/updateNeighbourhood', strict_slashes=False)
def node_updateNeighbourhood(node):
    return backend.healNode(node)

@app.route('/sensors/<int:node>/refresh', strict_slashes=False)
def refreshNode(node):
    return backend.refreshNode(node)

@app.route('/sensors/<int:node>/set/<int:param>/to/<int:value>', strict_slashes=False)
def set_config_param(node, param, value):
    return backend.set_node_config_param(node, param, value)

@app.route('/sensors/<int:node>/get/<int:param>', strict_slashes=False)
def get_config_param(node, param):
    return backend.get_node_config_param(node, param)

########################################################################################################################
############# SWITCHES #################################################################################################
########################################################################################################################

@app.route('/switches', strict_slashes=False)
def switches():
    switches = backend.get_switches()
    if type(switches) is str:
        return switches
    switches_list = ""
    for key, val in switches.items():
        switches_list += str(key) + "=" + str(val) + "\n"
    return Response(switches_list, mimetype="text/plain")

@app.route('/switches/<int:node>/<on_off_check>', strict_slashes=False)
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
        
        
@app.route('/devices', strict_slashes=False)
def devices():
    devices = backend.get_devices()
    if type(devices) is str:
        return devices
    devices_list = ""
    for key, val in devices.items():
        devices_list += str(key) + "=" + str(val) + "\n"
    return Response(devices_list, mimetype="text/plain")
    #return render_template("index.html")

@app.route('/sensors/add', strict_slashes=False)
@app.route('/switches/add', strict_slashes=False)
@app.route('/devices/add', strict_slashes=False)
def add_device():
    return backend.addDevice()

@app.route('/switches/remove', strict_slashes=False)
@app.route('/devices/remove', strict_slashes=False)
@app.route('/sensors/remove', strict_slashes=False)
def remove_device():
    return backend.removeDevice()

@app.route('/sensors/<int:node>/battery', strict_slashes=False)
@app.route('/devices/<int:node>/battery', strict_slashes=False)
def get_battery(node):
    return backend.battery(node)

@app.route('/sensors/<int:node>/setLocationTo/<value>', strict_slashes=False)
@app.route('/switches/<int:node>/setLocationTo/<value>', strict_slashes=False)
@app.route('/devices/<int:node>/setLocationTo/<value>', strict_slashes=False)
def set_node_location(node, value):
    return backend.set_node_location(node, value)

@app.route('/sensors/<int:node>/setNameTo/<value>', strict_slashes=False)
@app.route('/switches/<int:node>/setNameTo/<value>', strict_slashes=False)
@app.route('/devices/<int:node>/setNameTo/<value>', strict_slashes=False)
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
