import os
import subprocess
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5,GPIO.OUT)
GPIO.output(5,GPIO.LOW)
print("shutting down...the process")
subprocess.call(['shutdown','-h','now'],shell=False)