#!/usr/bin/env python
# -*- coding: utf-8 -*-

from signal import *

import requests 

import sys, getopt
from datetime import datetime
import time
import json
import os, fnmatch
from os.path import expanduser
import random

import re

esp_ip = "10.42.0.156"

def sendConfig():

   hostname = "129.69.185.197"
   topic_pub = "SENSOR/123412341234123412341234"
   topic_splitted = topic_pub.split('/')
   component = topic_splitted [0]
   component_id = topic_splitted [1]


   URL = "http://"+esp_ip+":80/config"

   data = "{'ip': '"+hostname+"', 'topic': '"+topic_pub+"','component': '"+component+"','componentId': '"+component_id+"'}"

   r = requests.post(url = URL, data = data) 

   # extracting response text  
   pastebin_url = r.text 
   print("The pastebin URL is:%s"%pastebin_url) 

def sendStatus(status):

   URL2 = "http://"+esp_ip+":80/status"

   data = "{'status': '"+status+"'}"

   r = requests.post(url = URL2, data = data) 

   # extracting response text  
   pastebin_url = r.text 
   print("The pastebin URL is:%s"%pastebin_url) 

def clean(*args):
   sendStatus(esp_ip, "off")
   sys.exit(0)

############################
# MAIN
############################
def main(argv):

   for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
      signal(sig, clean)

   hostname = 'localhost'
   topic_pub = 'test'

   #Read other measure interval from parameter data
   paramArray = json.loads(argv[0])
   for param in paramArray:
      if not ('name' in param and 'value' in param):
         continue
      elif param["name"] == "esp":
         esp_ip = param["value"]
   
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

   sendConfig()
   sendStatus("on")

   while True:
      time.sleep(10)
   

if __name__ == "__main__":
   main(sys.argv[1:])
