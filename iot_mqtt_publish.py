#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2016, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# smart_camera.py
# Take photo and upload file to imagga service then speak the result of tag
#
# Author : sosorry
# Date   : 18/04/2015

import thread
import json
import time
import os
import paho.mqtt.client as mqtt

# device id:
# sensor:
device = #"IOT_DEVICE_ID"
apikey = #"IOT_PROJECT_KEY or IOT_DEVICE_KEY" 

client = None

# The callback for when the client receives a CONNACK response from the server.
def on_connect(c, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #print "subscribe:"+"/v1/device/"+device+"/sensor/"+sensor_btn+"/rawdata"
    #client.subscribe("/v1/device/"+device+"/sensor/"+sensor_btn+"/rawdata")

    #publish
    data=[{"id":"pm1","value":[9]}]
    client.publish("/v1/device/"+device+"/rawdata", json.dumps(data))

# The callback for when a PUBLISH message is received from the server.
def on_message(c, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload)

if __name__ == "__main__":
    
    auth = {'username':apikey,'password':apikey}
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(apikey,apikey)
    
    try:
        client.connect("iot.cht.com.tw",1883, 60)
        client.loop_forever()
    except Exception as e:
        print("MQTT Broker is not online. connect later."+e.__str__())
    