import os
import subprocess
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.IN)

while True:
    val = GPIO.input(6)
    print(val)
    if val==1:
        break;
    time.sleep(0.2)

print(' finished ' )
    
