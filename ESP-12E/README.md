# ESP-12E

## NodeMCU

![NodeMCU](nodemcu.jpg)


## Install (Windows)

[Windows V3.4 driver](https://wiki.wemos.cc/_media/ch341ser_win_3.4.zip)
[Arduino IDE](https://www.arduino.cc/en/Main/Software)
[Python 2.7](https://www.python.org/download/releases/2.7/)

In Arduino IDE

Go to File > Preferences

Add `https://arduino.esp8266.com/stable/package_esp8266com_index.json` to Additional Boards Manager URLs 

![Preferences](preferences.png)

Go to Tools > Boards: "..." > Boards Manager 

![Board](board.png)

And select esp8266 Community

![Boards Manager](boardinfo.png)

## Using 

Go to Tools > Boards: "..." > NodeMCU 1.0 (ESP12-E Module)

![Select Board](selectboard.png)

Change Upload Speed to 9600

![Upload Speed](upspeed.png)

## First example

Select Blink application example from Arduino

![Blink](blink.png)

Change `LED_BUILTIN` to `4`

Build the circuit of the photo to test

![Example 1](ex1.jpg)

And upload to NodeMCU





