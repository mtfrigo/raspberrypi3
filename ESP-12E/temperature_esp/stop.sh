#!/bin/bash
sudo kill -9 $(ps -ef | grep sensoradapter_temp_nodemcu_stub.py | grep -v grep | awk '{print $2}')
