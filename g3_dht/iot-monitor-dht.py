#!/usr/bin/python
"""
Using PMS3003-G3, DHT22, LED Sensors and uploading rawdata to CHT IoT
- pms3003-g3 download from https://github.com/Thomas-Tsai/pms3003-g3
- DHT 11/22 download from https://github.com/adafruit/Adafruit_Python_DHT
CHT IoT
- RESTful upload rawdata
- MQTT registry to listen iotkey and deviceId
"""
import time
import datetime
import os
import requests
import requests.packages.urllib3
import json
import thread
import g3
import Adafruit_DHT
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

iotkey="DKW39G295W2UTUTXHP"
device="860607757"
productCode="lass"
serialId="1060100001"
ledPin = 7

client = None

newData = False

requests.packages.urllib3.disable_warnings()
air=g3.g3sensor()

GPIO.setmode(GPIO.BOARD)    ## Define pin numbering (Use board pin numbering)
GPIO.setup(ledPin, GPIO.OUT)     ## Setup GPIO Pin 7 to OUT 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print "subscribe:"+"/v1/registry/"+productCode+serialId
    client.subscribe("/v1/registry/"+productCode+serialId)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global iotkey, device
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload)
    iotkey = data["ck"]
    device = data["deviceId"]

def on_disconnect(client, userdata, rc):
    print("mqtt disconnection")
    if rc != 0:
        print("Unexpected disconnection.")

def mqtt_client_thread(string, sleeptime, *args):
    global client, iotkey
    auth = {'username':iotkey,'password':iotkey}
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.username_pw_set(iotkey,iotkey)
    print "MQTT client connect"
    try:
        client.connect("iot.cht.com.tw",1883, 60)
    except:
        print "MQTT Broker is not online. connect later."

    client.loop_forever()

def show_led_thread(string, sleeptime, *args):
    global newData
    while(True):
        if(newData):
            GPIO.output(ledPin,True)## Switch on pin 7
            #print 'led on:{0}_{1}\n'.format(string, sleeptime)
            time.sleep(sleeptime)
            #print 'led off:{0}_{1}\n'.format(string, sleeptime)
            GPIO.output(ledPin,False)## Switch off pin 7
            newData = False
        time.sleep(1)

if __name__ == "__main__":
    thread.start_new_thread(mqtt_client_thread, ("ThreadMqtt",1))
    thread.start_new_thread(show_led_thread, ("ThreadLed",3))
    
    try:
        while True:
            print("read g3")
            try:
                pmdata=air.read("/dev/ttyAMA0")
            except:
                print("exception:read g3")
                pmdata=[0,0,0,0,0,0]
                time.sleep(5)
                continue

            #params = urllib.urlencode({'field1': pmdata[3], 'field2': pmdata[4], 'field3': pmdata[5], 'key':'YOUR WRITE KEY'})
            #headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            # cht iot
            print("Get PMS3003-G3 Values:")
            print pmdata
            newData = True
            #DHT 22
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "18")
            if humidity is not None and temperature is not None:
                #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                print('Temp={0:0.1f},Humidity={1:0.1f}'.format(temperature, humidity))
            else:
                print('Failed to get reading. Try again!')

            headers = {"accept": "application/json","CK": iotkey}
            try:
                print("Send values to iot:"+device)
                #pm1, pm10, pm25,temperature,humidity
                data=[{"id":"pm1","save":True,"value":[pmdata[3]]},{"id":"pm10","save":True,"value":[pmdata[4]]},{"id":"pm25","save":True,"value":[pmdata[5]]},{"id":"temperature","save":True,"value":['{0:0.1f}'.format(temperature)]},{"id":"humidity","save":True,"value":['{0:0.1f}'.format(humidity)]}]
                url="https://iot.cht.com.tw/iot/v1/device/"+device+"/rawdata"
                response = requests.post(url, data=json.dumps(data), headers=headers)
                #print("result:"+response.status_code)
                print(response.status_code)
            except:
                print("exception: iot rawdata")
                time.sleep(5)
                continue
            #print("end")
            #seconds
            time.sleep(15)
        print("out of while")
    finally:                                                                                          
        GPIO.cleanup() 