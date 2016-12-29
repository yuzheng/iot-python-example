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

import RPi.GPIO as GPIO
import requests
import picamera
import json
import time
import os

headers = { 
    "accept": "application/json",

    #
    # REPLACE "authorization: "Basic ..." WITH YOUR AUTHORIZATION (api_key:api_secret)
    #
    "CK": "PKXT2XGTMRFK3T9YXT"
    }   

# device id:281156861
# sensor:camera01

BTN_PIN = 11
GPIO.setmode(GPIO.BOARD)    # Define pin numbering
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def mycallback(self):    
    with picamera.PiCamera() as camera:
        print("Take photo...")
        camera.resolution = (640, 480)
        camera.capture("test.jpg")
        files = {"file": open("test.jpg", "rb"), "meta":('',json.dumps({"id":"camera01","value":["Raspberry pi camera"]}), 'application/json')}
        #,"meta":({"id":"camera01","value":["Raspberry pi camera"]}
        
        #
        # replace "authorization: "Basic ..." with your Authorization (api_key:api_secret)
        #
        print("Upload photo...")
        #url = "http://api.imagga.com/v1/content"
        url="https://iot.cht.com.tw/iot/v1/device/281156861/snapshot"
        response = requests.post(url, files=files, headers=headers)
        print(response.text.encode("ascii"))
        #data = json.loads(response.text.encode("ascii"))

        #print("Get tags...")
        #url = "http://api.imagga.com/v1/tagging"
        #querystring = {"content": data["uploaded"][0]["id"]}
        #response = requests.request("GET", url, headers=headers, params=querystring)
        #data = json.loads(response.text.encode("ascii"))
        #obj = data["results"][0]["tags"][0]["tag"].encode("ascii")
        #print("<< " + obj + " >>")
        #cmd = "echo " + obj + " | festival --tts"
        #os.system(cmd)
        print("===============")


GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, callback=mycallback, bouncetime=2000)

try:
    while True:
        time.sleep(10)

finally:                                                                                          
    GPIO.cleanup()     

