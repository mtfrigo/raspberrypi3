import sys
import time
import datetime
import RPi.GPIO as GPIO
import tm1637
 
Display = tm1637.TM1637(4,5,tm1637.BRIGHT_TYPICAL)
 
Display.Clear()
Display.SetBrightnes(1)
 
while(True):
   now = datetime.datetime.now()
   hour = now.hour
   minute = now.minute
   second = now.second
   currenttime = [ 1, 1, 1, 1 ]
 
   Display.Show(currenttime)
   Display.ShowDoublepoint(second % 2)
 
   time.sleep(1)
