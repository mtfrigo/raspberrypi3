import RPi.GPIO as GPIO
import spidev
from time import sleep
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 1      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
 
# Initialisiere Potentiometer auf Analogen-PIN 0 und LED auf Digitalen PIN 4
temp = 0
led = 4
 
spi = spidev.SpiDev()
spi.open(0,0)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
 
def readadc(adcnum):
    # SPI-Daten auslesen
    r = spi.xfer2([1,8+adcnum <<4,0])
    adcout = ((r[1] &3) <<8)+r[2]
    return adcout
 
def changeLedColor(strip, color):
    strip.setPixelColor(0, color)
    strip.show()

def util_map(value, from_min, from_max, to_min, to_max):
        from_range = from_max - from_min
        to_range = to_max - to_min

        proportion = from_range*1.0 / to_range*1.0
        
        final = (value / proportion) - to_min
        return int(final)

if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()


    b = int(input("What is b? "))
    g = int(input("What is g? "))
    r = int(input("What is r? "))

    changeLedColor(strip, Color(b, g, r))


    while True:
        value = readadc(temp)
        x = util_map(value, 0, 1023, 0, 254)
        color = Color(255-x, 0, x)


        print("Value: " + str(value) + " ; x: " + str(x))

        #strip.setBrightness(brightness)
        changeLedColor(strip, color)
        
        sleep(0.5)