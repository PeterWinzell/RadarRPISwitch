#radar-sensor
#from gpiozero import DigitalInputDevice
from gpiozero import MotionSensor

import datetime
import time
import os

from picamera import PiCamera
from signal import pause




#set GPIO17 to recieve motion signal , set PIN to low to match sensor.
# also set reset time to 5 seconds.
#radar = DigitalInputDevice(17,pull_up=False,bounce_time = 5.0)
radar = MotionSensor(17)
# retrive camera object
camera = PiCamera()
camera.resolution =  (1024,768)

#motion counter
counter = 0

# shoot the image and timestamp the event for the filename
def detector():
    
    timestamp = str((datetime.datetime.now()))
    timestamp = timestamp[0:19]
    print("image captured at", timestamp)
    filename = "/home/pi/radar-sensor/pic" + str(counter) + ".jpg"
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

camera.start_preview()
while (counter < 3):
    #radar.when_activated = detector
    #radar.wait_for_motion()
    print("shooting")
    detector()
    time.sleep(10)
    counter = counter + 1
print("shooting done")
camera.stop_preview()
camera.close()
time.sleep(5)
print("shutting down")
#subprocess.call(['shutdown','-h','now'],shell=False)
    
