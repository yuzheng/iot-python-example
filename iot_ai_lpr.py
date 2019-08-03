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

apikey = ''

def faceage(inputImg):  
    global apikey
    headers = { 
        "X-API-KEY": apikey
        }
    files = {"file": open(inputImg, "rb")}
        
    print("Upload photo...")
    #url="https://iottl.cht.com.tw/apis/CHTIoT/ivs-lpr/v1/snapshot"
    url="https://iot.cht.com.tw/apis/CHTIoT/ivs-lpr/v1/snapshot"
    response = requests.request("POST", url, files=files, headers=headers)
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





