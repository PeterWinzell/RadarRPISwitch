#from gpiozero import DigitalInputDevice
from gpiozero import MotionSensor

import datetime
import time
import os
import subprocess
import sys

from threading import Thread
from picamera import PiCamera
from signal import pause
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(3,GPIO.IN)

while True:       
    if (GPIO.input(3) == True):
        print("GPIO 3 Open,pin 5")
        #break;
    else:
        print("GPIO 3 Closed,pin 5")
    time.sleep(0.5)
    