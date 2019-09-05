#!/bin/bash
cd $1
nohup python3 sensoradapter_temp_nodemcu_stub.py > start.log &
