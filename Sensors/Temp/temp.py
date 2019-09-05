import spidev
import paho.mqtt.client as mqtt
from time import sleep
 
# Initialisiere Temp-Sensor auf Analogen-PIN 0
temp = 0
 
spi = spidev.SpiDev()
spi.open(0,0)

broker_address="localhost"

client = mqtt.Client("P1")
client.connect(broker_address, 1883, 60)

client.loop_start()
 
def readadc(adcnum):
# SPI-Daten auslesen
    r = spi.xfer2([1,8+adcnum <<4,0])
    adcout = ((r[1] &3) <<8)+r[2]
    return adcout

try:
    while True:
        value = readadc(temp)
        volts = (value * 3.3) / 1024
        temperature_C = (volts - 0.5) * 100
 
        print("Temperature: " + str(round(temperature_C,2)) +  " C")
        client.publish("test", "Temperature: " + str(round(temperature_C,2)) +  " C")
        
        sleep(1)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
