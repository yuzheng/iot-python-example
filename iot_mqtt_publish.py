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


import json
import time
import paho.mqtt.client as mqtt

# device id:
# sensor:
host = "iot.cht.com.tw"  #"iot.cht.com.tw"
device = "860607757" #"IOT_DEVICE_ID"
sensor = "pm1"  #"IOT_SENSOR_ID"
apikey = "PKW18D323TG30UPNRT" #"IOT_PROJECT_KEY or IOT_DEVICE_KEY" 

client = None

def test_publish():
    for num in range(0,100,1):
        print("num:" + str(num))
        data=[{"id":sensor,"value":[num]}]
        client.publish("/v1/device/"+device+"/rawdata", json.dumps(data), qos=1)
        time.sleep(10)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(c, userdata, flags, rc):
    
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #print "subscribe:"+"/v1/device/"+device+"/sensor/"+sensor_btn+"/rawdata"
    #client.subscribe("/v1/device/"+device+"/sensor/"+sensor_btn+"/rawdata")
    client.subscribe("/v1/device/"+device+"/sensor/"+sensor+"/rawdata")

    #publish
    print("device:"+device)
    data=[{"id":sensor,"value":[9]}]
   
    print("/v1/device/"+device+"/rawdata")
    print(json.dumps(data))
    
    client.publish("/v1/device/"+device+"/rawdata", json.dumps(data))
    #client.publish.single("/v1/device/"+device+"/rawdata", json.dumps(data), qos = 1,hostname=host,port=1883, client_id=client_id,auth = {'username':apikey, 'password':apikey})
    
    print("aaa")
    time.sleep(1)
    test_publish()

def on_disconnect(c, userdata, rc):
    print("disconnecting reason  "  +str(rc))

def on_log(client, userdata, level, buf):
    print("log:" + str(level) + str(buf))

def mqtt_client_thread(string, sleeptime, *args):
    global client
    auth = {'username':apikey,'password':apikey}
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(apikey,apikey)
    print("MQTT client connect")
    try:
        client.connect(host,1883, 60)
        client.loop_forever()
    except:
        print("MQTT Broker is not online. connect later.")

# The callback for when a PUBLISH message is received from the server.
def on_message(c, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload)

if __name__ == "__main__":
    #thread.start_new_thread(mqtt_client_thread, ("ThreadMqtt",1))

    print("main")
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    auth = {'username':apikey,'password':apikey}
    client = mqtt.Client(client_id=client_id)  #, protocol=mqtt.MQTTv311
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log
    client.on_message = on_message
    client.username_pw_set(username=apikey,password=apikey)
    
    try:
        client.connect(host,1883, keepalive=60)
        client.loop_forever()
        #client.loop_start()
    except Exception as e:
        print("MQTT Broker is not online. connect later."+e.__str__())
