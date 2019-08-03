# -*- coding: utf-8 -*-
import sys
import getopt
import json
import paho.mqtt.client as mqtt

MQTTHOST = "iot.cht.com.tw"
MQTTPORT = 1883
mqttClient = mqtt.Client()
sensorId = "+"
deviceId = "" #860607757
apikey = ""  #PKXT2XGTMRFK3T9YXT


# 连接MQTT服务器
def on_mqtt_connect():
    mqttClient.username_pw_set(username=apikey,password=apikey)
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()
    #mqttClient.loop_forever()


# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)

# 消息处理函数
def on_message_come(lient, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload))


# subscribe 消息
def on_subscribe():
    mqttClient.subscribe("/v1/device/"+deviceId+"/sensor/"+sensorId+"/rawdata", 1) 
    mqttClient.on_message = on_message_come # 消息到来处理函数

def main(argv):
    global apikey
    global deviceId
    global sensorId
    
    try:
        opts, args = getopt.getopt(argv,"hk:i:d:s:",["apikey=","device=","sensor="])
    except getopt.GetoptError:
        print 'iot-mqtt-subscribe.py -k <apikey> -d <deviceId> -s <sensorId>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'iot-mqtt-subscribe.py -k <apikey> -d <deviceId> -s <sensorId>'
            sys.exit()
        elif opt in ("-k", "--apikey"):
            apikey = arg
        elif opt in ("-d", "--device"):
            deviceId = arg
        elif opt in ("-s", "--sensor"):
            sensorId = arg
    
    on_mqtt_connect()
    #data=[{"id":"cin","value":["test"]}]
    #on_publish("/v1/device/115355/rawdata", json.dumps(data), 1)
    on_subscribe()
    while True:
        pass

if __name__ == "__main__":
   main(sys.argv[1:])