import RPi.GPIO as GPIO
from time import sleep
 
buz = 15
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buz, GPIO.OUT)
 
#Die Tonhoehe kann mit Variation der Wartezeit (sleep) veraendert werden
while True:
        GPIO.output(buz, True)
        sleep(0.0005)
        GPIO.output(buz, False)
        sleep(0.0005)