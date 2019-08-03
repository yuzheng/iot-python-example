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
product = '' #lass
sn = ''  #1060100001

def aep_product():
    global apikey, product, sn
    
    headers = { 
        "accept": "application/json",
        "X-API-KEY": apikey
        }      
    
    print("GET Product info..." + product)
    print(product)
    url="https://iot.cht.com.tw/apis/CHTIoT/aep/v1/product/"+product+"/thing/"+sn
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    print(response.text) #.encode("ascii")
        
    print("===============")

def main(argv):
    global apikey, product, sn
    
    try:
        opts, args = getopt.getopt(argv,"hk:p:s:",["apikey=","product=","sn="])
    except getopt.GetoptError:
        print 'iot_aep_product.py -k <apikey> -p <product> -s <sn>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'iot_aep_product.py -k <apikey> -p <product> -s <sn>'
            sys.exit()
        elif opt in ("-k", "--apikey"):
            apikey = arg
        elif opt in ("-p", "--product"):
            product = arg
        elif opt in ("-s", "--sn"):
            sn = arg
    aep_product()

if __name__ == "__main__":
   main(sys.argv[1:])

