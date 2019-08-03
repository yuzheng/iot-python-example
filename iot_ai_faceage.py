#!/usr/bin/python
# Copyright (c) 2019, iot.cht.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# iot_ai_faceage.py
#
# Author : wyc
# Date   : 03/08/2019

import sys
import getopt
import requests
import json
import time
import base64 # for base64

apikey = ''

def faceage(inputImg):  
    global apikey
    headers = { 
        "accept": "application/json",
        "X-API-KEY": apikey
        }
    base64str = '';  
    with open(inputImg, "rb") as imageFile:
        base64str = base64.b64encode(imageFile.read())
    #print base64str
    payload = {"imgData":base64str}
        
    print("Upload photo...")
    url="https://iot.cht.com.tw/apis/CHTIoT/AgeGender/v1/face-age"
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.status_code)
    print(response.text) #.encode("ascii")
        
    print("===============")

def main(argv):
    global apikey
    inputImg = ''
    try:
        opts, args = getopt.getopt(argv,"hk:i:",["apikey=","input="])
    except getopt.GetoptError:
        print 'iot_ai_faceage.py -k <apikey> -i <input>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'iot_ai_faceage.py -k <apikey> -i <input>'
            sys.exit()
        elif opt in ("-k", "--apikey"):
            apikey = arg
        elif opt in ("-i", "--input"):
            inputImg = arg
    print inputImg
    faceage(inputImg)

if __name__ == "__main__":
   main(sys.argv[1:])





