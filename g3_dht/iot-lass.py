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
#import RPi.GPIO as GPIO

iothost="iot.cht.com.tw"

iotkey="YOUR CHT IOT DEVICE KEY"
device="YOUR CHT IOT DEVICE ID"

client = None

newData = False

requests.packages.urllib3.disable_warnings()
air=g3.g3sensor()

#GPIO.setmode(GPIO.BOARD)    ## Define pin numbering (Use board pin numbering)
#GPIO.setup(ledPin, GPIO.OUT)     ## Setup GPIO Pin 7 to OUT 

def post_iot_rawdata(pmdata):
    rawdatas=[]
    #DHT 22
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, "18")
    rawdata = None
    if humidity is not None and temperature is not None:
        print('T={0:0.1f},H={1:0.1f}'.format(temperature, humidity))
        rawdata = [{"id":"temperature","save":True,"value":['{0:0.1f}'.format(temperature)]},{"id":"humidity","save":True,"value":['{0:0.1f}'.format(humidity)]}]
    else:
        print('Get DHT fail!')
    if rawdata != None:
        rawdatas = rawdatas + rawdata
    
    #pm1, pm10, pm25,temperature,humidity
    #data=[{"id":"pm1","save":True,"value":[pmdata[3]]},{"id":"pm10","save":True,"value":[pmdata[4]]},{"id":"pm2_5","save":True,"value":[pmdata[5]]},{"id":"temperature","save":True,"value":['{0:0.1f}'.format(temperature)]},{"id":"humidity","save":True,"value":['{0:0.1f}'.format(humidity)]}]
    if pmdata[3] == 0 and pmdata[4] == 0 and pmdata[5] == 0:
        #data=[{"id":"temperature","save":True,"value":['{0:0.1f}'.format(temperature)]},{"id":"humidity","save":True,"value":['{0:0.1f}'.format(humidity)]}]
        rawdata = None
    else:
        rawdata = [{"id":"pm1","save":True,"value":[pmdata[3]]},{"id":"pm10","save":True,"value":[pmdata[4]]},{"id":"pm2_5","save":True,"value":[pmdata[5]]}]
    if rawdata != None:
        rawdatas = rawdatas + rawdata
    
    #post to iot
    try:
        headers = {"accept": "application/json","CK": iotkey}
        url="https://"+iothost+"/iot/v1/device/"+device+"/rawdata"
        response = requests.post(url, data=json.dumps(rawdatas), headers=headers, timeout=5.0)
        print(response.status_code)
    except:
        print("exception: iot rawdata")

if __name__ == "__main__":
    #thread.start_new_thread(show_led_thread, ("ThreadLed",3))
    
    passv=0
    try:
        while True:
            try:
                pmdata=air.read("/dev/ttyS0")
                newData = True
                print("Get:")
                print pmdata
            except:
                print("Get G3 Fail")
                pmdata=[0,0,0,0,0,0]
                if passv < 5 :
                    passv=passv+1
                    time.sleep(3)
                    continue
                else:
                    passv=0

            post_iot_rawdata(pmdata)
            time.sleep(15)
        print("end")
    finally:  
        print("final")                                                                                        
        #GPIO.cleanup() 
