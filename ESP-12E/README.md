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

<img src="./preferences.png" width="500">

Go to Tools > Boards: "..." > Boards Manager 

<img src="./board.png" width="500">

And select esp8266 Community

<img src="./boardinfo.png" width="500">

## Using 

Go to Tools > Boards: "..." > NodeMCU 1.0 (ESP12-E Module)

<img src="./selectboard.png" width="500">

Change Upload Speed to 9600

<img src="./upspeed.png" width="500">

## First example

Select Blink application example from Arduino

![Blink](blink.png)

Change `LED_BUILTIN` to `4`

Build the circuit of the photo to test


<img src="./ex1.jpg" width="200">
<img src="./ex1_2.jpg" width="200">

And upload to NodeMCU

## Utils

<img src="./nodemcu-pinout.jpg" width="500">





