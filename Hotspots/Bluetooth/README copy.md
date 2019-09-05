# XDK Bluetooth adapter

This folder contains adapter scripts for reading light sensor values from a Bosch XDK device via Bluetooth. The hardware setup for this adapter corresponds to:

 - a Raspberry Pi 3B (Stretch or Buster) configured as Bluetooth Hotspot (link of hotpost configuration)
 - a XDK Bosch device running the BLE project 

The following files are provided in this folder:
 
 - `BLE.zip`: This file contains the Bluetooth Low Energy Project which should be import to XDK.
 
 - `sensoradapter_bluetooth_stub.py`: This file contains a MQTT client, which publishes the values from XDK's sensor to a configured topic on MBP Broker and contains the bluetooth implementation to receive XDK sensor's values.

 - `install.sh`: This file installs the necessary libraries to run the python script.
 
 - `start.sh`: This file starts the execution of the python script.
 
 - `running.sh`: This file checks if the python script is running.
  
 - `stop.sh`: This file stops the execution of the python script.

## XDK Device Setup

The XDK Workbench version used is 3.6.0.

To import/export a project to XDK device see https://developer.bosch.com/web/xdk/importing-a-project

## Script details

The script `sensoradapter_bluetooth_stub.py` tries to connect to a XDK device that have "XDK" as prefix in its device name. If the environment  has more than one device with this prefix, you must use `sensoradapter_bluetooth_param` script and send the XDK MAC address by parameter on the MBP.

