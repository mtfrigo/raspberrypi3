from bluepy import btle
from bluepy.btle import Peripheral, Scanner, DefaultDelegate, BTLEException


import time
import binascii
import re

#
deviceScan = []

#Variable containing last iteration value from sensor
sensorValue = 0

# these are the byte values that we need to write to subscribe/unsubscribe for notifications
subscribe_bytes = b'\x01\x00'
unsubscribe_bytes = b'\x00\x00'

# handles of services
write_handle = None
subscribe_handle = None

# NOTE - MUST set this appropriately, depending on the type of address that the peripheral is advertising
# addr_type = bluepy.btle.ADDR_TYPE_PUBLIC
addr_type = btle.ADDR_TYPE_RANDOM


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):

        data = re.findall(r'\d+', data)[0]

        global sensorValue

        #if sensorValue != data:
        sensorValue = data
        print "A notification was received:  ", sensorValue

def scan(timeScan = 5):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(timeScan)
    global deviceScan
    deviceScan = []

    for dev in devices:
        print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Complete Local Name":
                deviceScan.append({
                    'name': value,
                    'id': dev.addr
                })
            print "  %s = %s" % (desc, value)

    print "\nDevice list: "
    index = 0
    for dev in deviceScan:
        print "%d) Device name: %s;\tID: %s" % (index, dev['name'], dev['id'])
        index+=1

    print "\n"

def connectToDevice(address):
    print "Connecting..."
    return btle.Peripheral(address,"random")

scan()

print('Enter the device number:')
x = input()

MAC_ADDRESS = deviceScan[x]['id']

#p = connectToDevice(MAC_ADDRESS)

# Connect to the peripheral
print "Connecting..."
p = Peripheral(MAC_ADDRESS, addr_type)

# Set the notification delegate
p.setDelegate(MyDelegate())

   # 0c68d100-266f-11e6-b388-0002a5d5c51b
   # 1ed9e2c0-266f-11e6-850b-0002a5d5c51b

service_uuid = "b9e875c0-1cfa-11e6-b797-0002a5d5c51b"
char_read_uuid = "1ed9e2c0-266f-11e6-850b-0002a5d5c51b"
char_write_uuid = "0c68d100-266f-11e6-b388-0002a5d5c51b"

svc = p.getServiceByUUID(service_uuid)

# Enable notification for read ch

# finding descriptors
print "Finding descriptors..."
time.sleep(1.0) # Allow sensor to stabilise

descs = svc.getDescriptors()

while write_handle is None and subscribe_handle is None:
    for desc in descs:
        print("  desc: " + str(desc.uuid) )
        str_uuid = str(desc.uuid).lower()

        if str_uuid == char_read_uuid:
            ch_read = svc.getCharacteristics(char_read_uuid)[0]
            subscribe_handle = desc.handle
            print("*** Found subscribe handle: " + str(subscribe_handle))
        elif str_uuid == char_write_uuid:
            ch_write = svc.getCharacteristics(char_write_uuid)[0]
            
            # Unable the sensor
            ch_write.write("0")
            
            write_handle = desc.handle
            print("*** Found write handle: " + str(write_handle))

    if write_handle is None or subscribe_handle is None:
        print "Some handle missing... Trying again..."

print "Subscribing to notifications..."
response = p.writeCharacteristic(subscribe_handle, subscribe_bytes, withResponse=True)
time.sleep(1.0) # Allow sensor to stabilise


try:
    
    print "Turning on sensor..."
    ch_write.write("1")
    time.sleep(1.0) # Allow sensor to stabilise

    while True:

        #print ch_read.read()
        if p.waitForNotifications(1.0):
            # handleNotification() was called
            continue

        print "Waiting..."

except KeyboardInterrupt:
    print "Stopping..."

    response = p.writeCharacteristic(subscribe_handle, unsubscribe_bytes, withResponse=True)

    print "Unsubscribing..."
    time.sleep(1.0) # Allow sensor to stabilise

    ch_write.write("0")

    print "Turning off the sensor..."
    time.sleep(1.0) # Allow sensor to stabilise

    p.disconnect()
    print "Disconnecting..."
    time.sleep(1.0) # Allow sensor to stabilise

except BTLEException as e:
    try:
        print "Device disconnected... Trying reconnect..."
        p = Peripheral(MAC_ADDRESS, addr_type)
        print "Reconnected..."
    except Exception as ex2:
        print("Second connection try failed")
        raise
    print(e)


