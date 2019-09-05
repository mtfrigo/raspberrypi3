#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, getopt
from datetime import datetime
import time
import json
import os, fnmatch
from os.path import expanduser
import random

import re
from bluepy import btle
from bluepy.btle import Peripheral, Scanner, DefaultDelegate, BTLEException
from binascii import hexlify
import binascii

from threading import Thread

class Bluepy(DefaultDelegate):
   def __init__(self):
      DefaultDelegate.__init__(self)

      self._peripheral_address = None
      self._peripheral_address_type = btle.ADDR_TYPE_PUBLIC
      self._peripheral = None

      self._scanner = Scanner().withDelegate(self)
      self._devicesScanned = []

      self._service_uuid = "b9e875c0-1cfa-11e6-b797-0002a5d5c51b"
      self._char_read_uuid = "1ed9e2c0-266f-11e6-850b-0002a5d5c51b"
      self._char_write_uuid = "0c68d100-266f-11e6-b388-0002a5d5c51b"

      self._descs = None
      self._svc = None

      self._ch_read = None
      self._ch_write = None

      self.lastValue = {}
      self.lastValue['value'] = 0
      self.lastValue['datetime'] = "oi"

   def reset(self):
      self._peripheral = None
      self._descs = None
      self._svc = None

      self._ch_read = None
      self._ch_write = None

   def scan(self, time=3):

      devices = self._scanner.scan(time)

      for dev in devices:
         print ("Device "+dev.addr+" ("+dev.addrType+"), RSSI="+str(dev.rssi)+" dB")
         for (adtype, desc, value) in dev.getScanData():
            if desc == "Complete Local Name":
               self._devicesScanned.append({
                  'name': value,
                  'id': dev.addr
               })

   def findXDKAddress(self):
      for dev in self._devicesScanned:
         if dev['name'].startswith( 'XDK' ):
            self._peripheral_address = dev['id']

      return self._peripheral_address

   def setXDKAddress(self, mac):
      self._peripheral_address = mac

   def handleNotification(self, cHandle, data):

      data = re.findall(r'\d+', str(data))[0]

      self.lastValue['value'] = data
      self.lastValue['datetime'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

      print ("Received data: "+ str(data))

      #self.lastValue = int(data)

   def handleDiscovery(self, dev, isNewDev, isNewData):
      if isNewDev:
         print ("Discovered device "+ dev.addr)
      elif isNewData:
         print ("Received new data from"+ dev.addr)

   def connect(self):

      triesCounter = 0

      while self._peripheral == None :

         try:
            print ('\nConnecting...')
            self._peripheral = Peripheral(self._peripheral_address, "random")
            if(self._peripheral != None):
               print ('Connected!')

         except BTLEException as e:
            triesCounter = triesCounter + 1
            print ("Number of tries: "+str(triesCounter))
            print ("Trying to connect again after 5s\n")
            print(e)
            time.sleep(5)

   def setDelegate(self):
      self._peripheral.setDelegate(self)

   def discoverSvc(self):
      while self._svc == None or self._descs == None or self._ch_read == None or self._ch_write == None:
         print ("\nFinding service...")
         self._svc = self._peripheral.getServiceByUUID(self._service_uuid)
         print ("Finding descriptors...")
         self._descs = self._svc.getDescriptors()
         print ("Finding read characteristic...")
         self._ch_read = self._svc.getCharacteristics(self._char_read_uuid)[0]
         print ("Finding write characteristic...\n")
         self._ch_write = self._svc.getCharacteristics(self._char_write_uuid)[0]

      print ("All characteristics found!!!\n")


   def enableSensor(self):
      print ("Turning sensor on...\n")
      self._ch_write.write(b'\x31')
      time.sleep(1.0)

   def disableSensor(self):
      print ("Turning sensor off...\n")
      self._ch_write.write(b'\x30')
      time.sleep(1.0)

   def disconnect(self):
      print ('Disconnecting...')

      self._peripheral.disconnect()

      self._peripheral = None
      print ('Disconnected!\n')
   
   def readValues(self):
      print ("Reading values...\n")

      count = 0
      while True:
         if self._peripheral.waitForNotifications(5.0):
            count = count + 1
            continue

   def BluetoothFlow(self):

      #self.scan(3)

      #xdk_address = self.findXDKAddress()

      #xdk_address = "f1:63:c2:c4:4b:fe"
      xdk_address = "f1:63:c2:c4:4b:fe"
      self.setXDKAddress(xdk_address)

      print ("\nXDK MAC: "+ xdk_address)

      disconnectCounter = 0
      active = True
      
      while active == True:
         try:
            self.reset()
            
            self.connect()
               
            self.setDelegate()

            self.discoverSvc()

            self.enableSensor()
                  
            try:
               self.readValues()
            except BTLEException as e:
               print(e)
               disconnectCounter = disconnectCounter + 1
               print ("\nDisconnection number: "+str(disconnectCounter))
               print ("\nTrying to reconnect after 5s...")
               time.sleep(5.0)

            except KeyboardInterrupt:
               active = False
               print ("\nStopping...")

         except BTLEException as e:
            print(e)

      self.disableSensor()
      self.disconnect()

   def getLastValue(self):
      return (self.lastValue)
      
############################
# MAIN
############################
def main(argv):

   xdk = Bluepy()

   bluepy_thread = Thread(target=xdk.BluetoothFlow)
   bluepy_thread.name = "BluetoothFlow"
   bluepy_thread.daemon = True

   bluepy_thread.start()

   lastValueSent = {}
   lastValueSent['value'] = 0
   lastValueSent['datetime'] = "ioi"

   try:  
      while True:

         # messages in json format
         # send message, topic: temperature
         t = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
         lastValue = xdk.getLastValue()

         if(lastValue and lastValueSent):

            if(lastValue['datetime'] != lastValueSent['datetime']):
               
               lastValueSent['value'] = lastValue['value']
               lastValueSent['datetime'] = lastValue['datetime']
               print("Value main: " + str(lastValue['value']))

         time.sleep(30)

   except:
      e = sys.exc_info()
      print ("end due to: ", str(e))
      
if __name__ == "__main__":
   main(sys.argv[1:])
