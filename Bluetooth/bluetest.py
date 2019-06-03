
import time
import sys
import argparse

from bluepy import btle
from bluepy.btle import Peripheral, Scanner, DefaultDelegate, BTLEException

            
class Bluepy(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

        self._peripheral_address = None
        self._peripheral_address_type = btle.ADDR_TYPE_PUBLIC
        self._peripheral = None

        self._scanner = Scanner().withDelegate(self)
        self._devicesScanned = []

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

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device "+ dev.addr)
        elif isNewData:
            print ("Received new data from"+ dev.addr)

    def connect(self):
        print ('Connecting...')
        self._peripheral = Peripheral(self._peripheral_address, "random")
        if(self._peripheral != None):
            print ('Connected!')

    def disconnect(self):
        print ('Disconnecting...')

        self._peripheral.disconnect()

        self._peripheral = None
        print ('Disconnected!')
        


def main():

    xdk = Bluepy()

    xdk.scan(3)


    xdk_address = xdk.findXDKAddress()

    print ("\nXDK MAC: "+ xdk_address)

    xdk.connect()

    time.sleep(5.0)

    xdk.disconnect()


if __name__ == "__main__":
    main()