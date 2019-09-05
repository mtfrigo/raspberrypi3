import RPi.GPIO as GPIO
 
#Initialisiere LED auf Digital-PIN 4 und Button auf Digital-PIN 15 & 16
led = 4
button1 = 15
button2 = 16
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)
 
while True:
    if GPIO.input(button1) == GPIO.HIGH:
        print("Botao high")
    if GPIO.input(button2) == GPIO.HIGH:
        print("Botao2 HIGH")
