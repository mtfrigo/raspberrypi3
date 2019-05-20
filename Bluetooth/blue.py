from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
import time
import binascii

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

def scan(timeScan = 5):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(timeScan)

    for dev in devices:
        print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
        for (adtype, desc, value) in dev.getScanData():
            print "  %s = %s" % (desc, value)

def connectToDevice(address):
    print "Connecting..."
    return btle.Peripheral(address,"random")

#scan()
p = connectToDevice("C2:F2:45:78:D3:41")
print "Services..."
for svc in p.services:
     print str(svc)

   # 0c68d100-266f-11e6-b388-0002a5d5c51b
   # 1ed9e2c0-266f-11e6-850b-0002a5d5c51b

lightSensor = btle.UUID("b9e875c0-1cfa-11e6-b797-0002a5d5c51b")

lightService = p.getServiceByUUID(lightSensor)
for ch in lightService.getCharacteristics():
    print str(ch)

uuidConfig = btle.UUID("0c68d100-266f-11e6-b388-0002a5d5c51b")
lightSensorConfig = lightService.getCharacteristics(uuidConfig)[0]
# Enable the sensor
lightSensorConfig.write("1")

uuidValue  = btle.UUID("1ed9e2c0-266f-11e6-850b-0002a5d5c51b")
lightSensorValue = lightService.getCharacteristics(uuidValue)[0]
# Read the sensor

time.sleep(1.0) # Allow sensor to stabilise

try:

    while True:
        val = lightSensorValue.read()
        #if("a0420020a5" != binascii.b2a_hex(val)):
        if("984d0020a5" != binascii.b2a_hex(val)):
            print "Light sensor raw value: ", val
        #time.sleep(0.1)

except KeyboardInterrupt:
    print "Disconnecting..."
    lightSensorConfig.write("0")
    p.disconnect()