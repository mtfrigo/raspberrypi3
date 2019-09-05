from bluepy.btle import Scanner, DefaultDelegate
from bluepy import btle
import time
import binascii
import re
from neopixel import *
import random

sensorValue = 0
colorLED = Color(0, 255, 0)

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
            print "Received new data from", dev.addrz

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):

        data = re.findall(r'\d+', data)[0]

        global sensorValue
        global colorLED

        if sensorValue != data:
            sensorValue = data
            colorLED = changeLEDColor()
            print "A notification was received:  ", sensorValue

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

def changeLEDColor():
    return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#scan()

 # Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()


MAC_ADDRESS = "E1:8A:B7:71:E5:6D"
p = connectToDevice(MAC_ADDRESS)
p.setDelegate(MyDelegate())

   # 0c68d100-266f-11e6-b388-0002a5d5c51b
   # 1ed9e2c0-266f-11e6-850b-0002a5d5c51b

service_uuid = "b9e875c0-1cfa-11e6-b797-0002a5d5c51b"
char_read_uuid = "1ed9e2c0-266f-11e6-850b-0002a5d5c51b"
char_write_uuid = "0c68d100-266f-11e6-b388-0002a5d5c51b"

svc = p.getServiceByUUID(service_uuid)
ch_read = svc.getCharacteristics(char_read_uuid)[0]
ch_write = svc.getCharacteristics(char_write_uuid)[0]

# Enable the sensor
ch_write.write("1")

# Enable notification for read ch
p.writeCharacteristic(ch_read.valHandle+1, "\x02\x00")

time.sleep(1.0) # Allow sensor to stabilise

try:

    strip.setPixelColor(0, colorLED)
    strip.show()

    while True:
        if p.waitForNotifications(1.0):
            strip.setPixelColor(0, colorLED)
            strip.show()
            continue

        print "Waiting..."

except KeyboardInterrupt:
    print "Disconnecting..."
    ch_write.write("0")
    p.disconnect()