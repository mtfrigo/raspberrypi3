#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import sys, getopt
from datetime import datetime
import time
import json
import os, fnmatch
from os.path import expanduser
import random

import re

############################
# MAIN
############################
def main(argv):

   hostname = 'localhost'
   topic_pub = 'test'
   
   configFileName = "connections.txt"
   topics = []
   brokerIps = []
   configExists = False

   configFile = os.path.join(os.getcwd(), configFileName)

   while (not configExists):
       configExists = os.path.exists(configFile)
       time.sleep(1)

   # BEGIN parsing file
   fileObject = open (configFile)
   fileLines = fileObject.readlines()
   fileObject.close()

   for line in fileLines:
       pars = line.split('=')
       topic = pars[0].strip('\n').strip()
       ip = pars[1].strip('\n').strip()
       topics.append(topic)
       brokerIps.append(ip)

   # END parsing file
   
   hostname = brokerIps [0]
   topic_pub = topics [0]
   topic_splitted = topic_pub.split('/')
   component = topic_splitted [0]
   component_id = topic_splitted [1]
   
   # --- Begin start mqtt client
   id = "id_%s" % (datetime.utcnow().strftime('%H_%M_%S'))

   app = Flask(__name__)

   @app.route('/time')
   def getTime():
      time = datetime.now()
      return "Hotspot date and time: " + str(time)

   @app.route('/brokerIp')
   def getBrokerId():
      return hostname

   @app.route('/brokerTopic')
   def getBrokerTopic():
      return topic_pub

   @app.route('/component')
   def getBrokerComponent():
      return component

   @app.route('/componentId')
   def getBrokerComponentId():
      return component_id

   @app.route('/status')
   def getBrokerStatus():
      return "on"

   app.run(host='0.0.0.0', port=8090)


if __name__ == "__main__":
   main(sys.argv[1:])
