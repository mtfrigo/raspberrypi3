from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
import time
import binascii

from neopixel import *

# LED strip configuration:
LED_COUNT      = 1      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

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

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
strip.setPixelColor(0, Color(255,0,0))
strip.show()

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
            #print "Light sensor raw value: ", val
            val = float(val)
            if(val > 0.4):
                print "valor MAIOR que 0.4: ", val
                strip.setPixelColor(0, Color(255,0,0))
                strip.show()
            else:
                print "valor MENOR que 0.4: ", val
                strip.setPixelColor(0, Color(0,0,255))
                strip.show()

        #time.sleep(0.1)

except KeyboardInterrupt:
    print "Disconnecting..."
    lightSensorConfig.write("0")
    p.disconnect()
    strip.setPixelColor(0, Color(0,0,0))
    strip.show()