# -*- coding: utf-8 -*-
import json
import paho.mqtt.client as mqtt

MQTTHOST = "localhost"
MQTTPORT = 1883
mqttClient = mqtt.Client()
apikey = "PKMZH2M0EXK7XWY51C"


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
    mqttClient.subscribe("/v1/device/115355/sensor/cin/rawdata", 1)
    mqttClient.on_message = on_message_come # 消息到来处理函数


def main():
    on_mqtt_connect()
    data=[{"id":"cin","value":["test"]}]
    on_publish("/v1/device/115355/rawdata", json.dumps(data), 1)
    on_subscribe()
    while True:
        pass



if __name__ == '__main__':
    main()
