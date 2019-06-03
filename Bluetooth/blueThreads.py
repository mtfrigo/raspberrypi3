#!/usr/bin/env python

from threading import Thread
import time

from bluepy import btle
from bluepy.btle import Peripheral, Scanner, DefaultDelegate, BTLEException

import time
import binascii
import re

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

class BluepyExample(DefaultDelegate):
    def __init__(self, address, type=btle.ADDR_TYPE_PUBLIC):
        DefaultDelegate.__init__(self)

        self._peripheral_address = address
        self._peripheral_address_type = type
        self._peripheral = None

        # start the bluepy IO thread
        self._bluepy_thread = Thread(target=self._bluepy_handler)
        self._bluepy_thread.name = "bluepy_handler"
        self._bluepy_thread.daemon = True

        self._write_handle = None
        self._subscribe_handle = None
        self._descs = None
        self._svc = None

        self._ch_read = None
        self._ch_write = None

        self._devicesScan = []

        self._service_uuid = "b9e875c0-1cfa-11e6-b797-0002a5d5c51b"
        self._char_read_uuid = "1ed9e2c0-266f-11e6-850b-0002a5d5c51b"
        self._char_write_uuid = "0c68d100-266f-11e6-b388-0002a5d5c51b"

        self.lastValue = 0

        self._status = "Inactive"

        self._bluepy_thread.start()


    def getLastValue(self):
        return self.lastValue
    
    def getStatus(self):
        return self._status

    def handleNotification(self, cHandle, data):

        data = re.findall(r'\d+', data)[0]

        self.lastValue = int(data)

        #print "A notification was received:  ", data

    def _scan(self):

        self._status = "Scanning"

        self._peripheral_address = None

        scanner = Scanner().withDelegate(ScanDelegate())

        while self._peripheral_address == None:
            devices = scanner.scan(5)

            self._devicesScan = []

            for dev in devices:
                print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
                for (adtype, desc, value) in dev.getScanData():
                    if desc == "Complete Local Name":
                        self._devicesScan.append({
                            'name': value,
                            'id': dev.addr
                        })
                    print "  %s = %s" % (desc, value)

            print "\nDevice list: "
            index = 0
            for dev in self._devicesScan:
                print "%d) Device name: %s;\tID: %s" % (index, dev['name'], dev['id'])
                index+=1
            print "\n"

            for dev in self._devicesScan:
                if dev['name'].startswith( 'XDK' ):
                    self._peripheral_address = dev['id']


    def _connect(self):

        self._status = "Trying connection"
        
        while self._peripheral == None:

            try:
                print "Connecting...\n"
                self._peripheral = btle.Peripheral(self._peripheral_address, self._peripheral_address_type)
            
            except BTLEException as e:
                print(e)
                print "Device disconnected... Trying reconnect...\n"
                time.sleep(5.0)

    def _disconnect(self):

        print "Stopping..."

        print "Turning off the sensor..."
        self._ch_write.write("0")
        time.sleep(1.0) 

        print "Disconnecting..."
        self._peripheral.disconnect()
        time.sleep(1.0) 

    def _bluepy_handler(self):
        """This is the bluepy IO thread
        :return:
        """
        try:

            while True:

                self._write_handle = None
                self._subscribe_handle = None
                self._descs = None
                self._svc = None
                self._peripheral = None

                self._scan()
                
                self._connect()
                
                # Set the notification delegate
                self._peripheral.setDelegate(self)
                
                self._svc = self._peripheral.getServiceByUUID(self._service_uuid)

                print "Finding descriptors...\n"
                self._descs = self._svc.d()
                time.sleep(1.0) # Allow sensor to stabilise

                while self._write_handle is None and self._subscribe_handle is None:
                    
                    for desc in self._descs:
                        print("  desc: " + str(desc.uuid) )
                        str_uuid = str(desc.uuid).lower()

                        if str_uuid == self._char_read_uuid:
                            self._ch_read = self._svc.getCharacteristics(self._char_read_uuid)[0]
                            self._subscribe_handle = desc.handle
                            print("*** Found subscribe handle: " + str(self._subscribe_handle))
                        elif str_uuid == self._char_write_uuid:
                            self._ch_write = self._svc.getCharacteristics(self._char_write_uuid)[0]
                            
                            # Unable the sensor
                            self._ch_write.write("0")
                            
                            self._write_handle = desc.handle
                            print("*** Found write handle: " + str(self._write_handle))

                    if self._write_handle is None or self._subscribe_handle is None:
                        print "Some handle missing... Trying again...\n"

                #print "Subscribing to notifications...\n"
                time.sleep(1.0) 

                try:

                    print "Turning on sensor...\n"
                    self._ch_write.write("1")
                    time.sleep(1.0) # Allow sensor to stabilise

                    print "Sensor ready!\n"
                    self._status = "Active"

                    while True:

                        #print ch_read.read()
                        if self._peripheral.waitForNotifications(1.0):
                            # handleNotification() was called
                            continue
                        #print "Waiting..."

                except BTLEException as e:
                    #try:
                    print(e)
                    print "Device disconnected... Trying reconnect...\n"
                    
                    self.lastValue = 0
                    time.sleep(5.0)

                except KeyboardInterrupt:
                    print "OI THREAD..."
                    example._disconnect()

        except BTLEException as e:
            print(e)
            



def main():

    mac = None
    addr_type = btle.ADDR_TYPE_RANDOM
    example = BluepyExample(mac, addr_type)

    try:

        while True:
            
            print "\nLast value: " + str(example.getLastValue())
            print "Status: " + str(example.getStatus())
            time.sleep(5.0)

    except KeyboardInterrupt:
            print "\nStopping..."

if __name__ == '__main__':main()