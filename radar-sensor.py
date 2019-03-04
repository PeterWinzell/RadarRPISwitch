#radar-sensor
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




#set GPIO17 to recieve motion signal , set PIN to low to match sensor.
# also set reset time to 5 seconds.
#radar = DigitalInputDevice(17,pull_up=False,bounce_time = 5.0)
#radar = MotionSensor(17)

# retrive camera object
camera = PiCamera()
camera.resolution =  (800,600)

#motion counter
counter = 0
#current file dir
filedir = "/home/pi/radar-sensor/RadarRPISwitch/pic"

mode = GPIO.getmode()
if mode == GPIO.BCM:
    print("BCM mode")
elif mode == GPIO.BOARD:
    print("Board mode")
else:
   print("no mode")


GPIO.setup(5,GPIO.OUT)
GPIO.output(5,GPIO.HIGH)
# shoot the image  and timestamp the event for the filename
def detector():
    
    timestamp = str((datetime.datetime.now()))
    timestamp = timestamp[0:19]
    print("image captured at", timestamp)
    filename = filedir + str(counter) + ".jpg"
    removefile(filename)
    camera.capture(filename)
    #camera.capture("pic.jpg")
    
    test()                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    
def test():
    print("motion detected ", counter)

def removefile(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(" file does not exist")


#start key listening thread
#thread = Thread(target = listenforbreakkey,args=[])

camera.start_preview()
try:
    while (counter < 3):
        #radar.when_activated = detector
        #radar.wait_for_motion()
        print("shooting")
        detector()
        time.sleep(10)
        counter = counter + 1
except KeyboardInterrupt:        
    print("interruption by keyboard")
    camera.stop_preview()
    camera.close()
    sys.exit()
    
camera.stop_preview()
camera.close()


#time.sleep(60)
GPIO.output(5,GPIO.LOW)
print("shutting down...you got one minute to kill the process")
#subprocess.call(['shutdown','-h','now'],shell=False)
    
