import RPi.GPIO as GPIO
import spidev
from time import sleep
  
# Initialisiere SoundSensor auf analogen A0 und LED auf digitalen PIN 4
sound = 0
led = 4
  
spi = spidev.SpiDev()
spi.open(0,0)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sound, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
  
def readadc(adcnum):
# SPI-Daten auslesen
    r = spi.xfer2([1,8+adcnum <<4,0])
    adcout = ((r[1] &3) <<8)+r[2]
    return adcout
 
#LED wird ab einem gewissen Soundlevel aktiviert
#Sensitivitaet des Sensors kann mit "x > 250" veraendert werden
while True:
    x = readadc(sound)
    print x
    if(x > 250):
        print "> 250"

    else:
        print "<<<<< 250"

    sleep(1)

