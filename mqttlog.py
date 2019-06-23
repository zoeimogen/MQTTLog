#!/usr/bin/python3
# pylint: disable=invalid-name

import json
import csv
import logging
import os
from datetime import datetime
import paho.mqtt.client as mqtt

mqtt_user = os.environ['MQTT_USER']
mqtt_password = os.environ['MQTT_PASSWORD']
mqtt_host = os.environ['MQTT_HOST']
mqtt_port = int(os.environ['MQTT_PORT'])
mqtt_topic = os.environ['MQTT_TOPIC']

f = open(os.environ['OUTPUT'], 'a', buffering=1)
csvwriter = csv.writer(f)

def on_message(_, __, msg):
    global csvwriter
    message = msg.payload.decode('utf-8')
    logging.debug(message)
    data = json.loads(message)
    csvwriter.writerow([datetime.now().strftime('%c'),
                        data['pm10'],
                        data['pm25'],
                        data['temperature'],
                        data['humidity'],
                        data['pressure'],
                        data['gas']])

def on_connect(client, _, __, ___):
    client.subscribe(mqtt_topic, 0)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
mqttc = mqtt.Client()
mqttc.enable_logger()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.tls_set()
mqttc.tls_insecure_set(True)
mqttc.username_pw_set(mqtt_user, mqtt_password)
mqttc.connect(mqtt_host, mqtt_port)

mqttc.loop_forever()
