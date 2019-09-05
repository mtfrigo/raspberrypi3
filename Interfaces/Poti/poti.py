import RPi.GPIO as GPIO
import spidev
from time import sleep
 
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
adcout = ((r[1] &3) <<8)+r[2]return adcout
 
while True:
    value = readadc(temp)
    print("Value: " + str(value))
 
    if(value > 500):
        GPIO.output(led, True)
    else:
        GPIO.output(led, False)
    sleep(0.5)