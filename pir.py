import RPi.GPIO as GPIO
import time
import datetime
import requests
import requests.packages.urllib3
import picamera
import json
import os
import multiprocessing as mp


#multiprocessing.freeze_support()  # Windows need this line to avoid appearing RuntimeError
headers = { 
    "accept": "application/json",

    #
    # REPLACE "authorization: "Basic ..." WITH YOUR AUTHORIZATION (api_key:api_secret)
    #
    "CK": "DKASBB4ARHRXW13ACZ"
    }

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
LED_PIN = 12
PIR_PIN = 11
WAIT_TIME = 200
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_PIN, GPIO.OUT)

requests.packages.urllib3.disable_warnings()

def takePhoto():
    with picamera.PiCamera() as camera:
        print("Take photo...")
        camera.resolution = (640, 480)
        camera.rotation = 180
        camera.capture("test.jpg")
        files = {"file": open("test.jpg", "rb"), "meta":('',json.dumps({"id":"photo","value":["Raspberry pi camera"]}), 'application/json')}
        #,"meta":({"id":"camera01","value":["Raspberry pi camera"]}
        
        #
        # replace "authorization: "Basic ..." with your Authorization (api_key:api_secret)
        #
        print("Upload photo...")
        #url = "http://api.imagga.com/v1/content"
        url="https://iot.cht.com.tw/iot/v1/device/4401356075/snapshot"
        response = requests.post(url, files=files, headers=headers)
        print(response.text.encode("ascii"))
        print("===============")

def mycallback(channel):
    print str(datetime.datetime.now())," Motion detected @", time.ctime()
    #q = mp.Queue()
    #p = mp.Process(target=takePhoto, args=())
    #p.start()
    #p.join()

    pool = mp.Pool()
    pool.apply_async(takePhoto, args=())
    pool.close()
    pool.join()

    blink_led()
def blink_led():
    for i in xrange(3) :
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)

try:
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=mycallback, bouncetime=WAIT_TIME)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print "Exception: KeyboardInterrupt"

finally:
    GPIO.cleanup()
