#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

import sys, getopt
import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
import os, fnmatch
from os.path import expanduser
import random

import re


from threading import Thread

############################
# MQTT Client
############################
class mqttClient(object):
   hostname = 'localhost'
   port = 1883
   clientid = ''

   lastValue = 0

   def __init__(self, hostname, port, clientid):
      self.hostname = hostname
      self.port = port
      self.clientid = clientid

      # create MQTT client and set user name and password 
      self.client = mqtt.Client(client_id=self.clientid, clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
      #client.username_pw_set(username="use-token-auth", password=mq_authtoken)

      # set mqtt client callbacks
      self.client.on_connect = self.on_connect
      self.client.on_message = self.on_message

   # The callback for when the client receives a CONNACK response from the server.
   def on_connect(self, client, userdata, flags, rc):
      print("[" + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "]: " + "ClientID: " + self.clientid + "; Connected with result code " + str(rc))

   def on_message(self, client, userdata, message):
      self.lastValue = float(str(message.payload.decode("utf-8")))
      print("message received " ,str(message.payload.decode("utf-8")))
      print("message topic=",message.topic)
      print("message qos=",message.qos)
      print("message retain flag=",message.retain)

   # publishes message to MQTT broker
   def sendMessage(self, topic, msg):
      self.client.publish(topic=topic, payload=msg, qos=0, retain=False)
      print(msg)

   # connects to MQTT Broker
   def start(self):
      #self.client.connect(self.hostname, self.port, 60)
      self.client.connect(self.hostname, self.port, 60)
      self.client.subscribe("MTFESP")

      #runs a thread in the background to call loop() automatically.
      #This frees up the main thread for other work that may be blocking.
      #This call also handles reconnecting to the broker.
      #Call loop_stop() to stop the background thread.
      self.client.loop_start()

   def getLastValue(self):
      return self.lastValue

############################
# MAIN
############################
def main():

   hostname = "129.69.185.169"
   topic_pub = "test"
   component = "SENSOR"
   component_id = "123412341234123412341234"

   app = Flask(__name__)

   @app.route('/time')
   def getTime():
      time = datetime.now()
      return "Hotspot date and time: " + str(time)

   @app.route('/brokerIp')
   def getBrokerId():
      return "129.69.185.169"

   @app.route('/brokerTopic')
   def getBrokerTopic():
      return "test"

   app.run(host='0.0.0.0', port=8090)
      
if __name__ == "__main__":
   main()
