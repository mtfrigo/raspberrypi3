import RPi.GPIO as GPIO
import spidev
from time import sleep
  
# Initialisiere Joystick auf Analogen PINS 0 & 1
joyX = 0
joyY = 1
  
spi = spidev.SpiDev()
spi.open(0,0)
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
  
def readadc(adcnum):
# SPI-Daten auslesen
    r = spi.xfer2([1,8+adcnum <<4,0])
    adcout = ((r[1] &3) <<8)+r[2]
    return adcout
  
while True:
    x = readadc(joyX)
    y = readadc(joyY)
    print("X: " + str(x) + " Y: " + str(y))
    if(x > 1000):
        print("Joystick gedrueckt")
    sleep(0.1)