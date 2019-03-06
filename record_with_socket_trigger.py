# version 0.0.1 Peter Winzell jan 2019
import io
import picamera
import time
import picamera.array
import numpy as np
import subprocess
import fnmatch
import os
import json
import _thread
import firebase_admin
import RPi.GPIO as GPIO

from PIL import Image, ImageDraw

prior_image = None
camera = None

REC_RESOLUTION = (1280, 720) # the recording resolution
REC_FRAMERATE = 24           # the recording framerate
REC_SECONDS = 10             # number of seconds to store in ring buffer
REC_BITRATE = 1000000        # bitrate for H.264 encoder

MOTION_MAGNITUDE = 60        # the magnitude of vectors required for motion
MOTION_VECTORS = 10          # the number of vectors required to detect motion

MAX_MP4_FILES = 0           # the maximum number of files we are allowed to store
                    
BREAK_PIN = 6                # interrupt script, to be able to turn the script off while in a shut down wake loop. Just pinch a cable hooked up to BREAK_PIN
SHUT_PIN  = 5                # Set this pin to low when we want the pi to turn off power.


def setupGPIOS():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BREAK_PIN,GPIO.IN)
    GPIO.setup(SHUT_PIN,GPIO.OUT)
    GPIO.output(SHUT_PIN,GPIO.HIGH)

def write_before(stream):
    # Write the entire content of the circular buffer to disk. No need to lock
    # the stream here as we're definitely not writing to it simultaneously
    with io.open('before.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.header:
                stream.seek(frame.position)
                break
        while True:
            buf = stream.read1()
            if not buf:
                break
            output.write(buf)
    # Wipe the circular stream once we're done
    stream.seek(0)
    stream.truncate()

def getTimeStampedFileName():
    return time.strftime("report%Y%m%d-%H%M%S")
    #return "motion-detected"

def numFiles():
    return len(fnmatch.filter(os.listdir("videos/"),"*.mp4"))

# remove all previous mp4 files 
def removeOldestFile():
    if (numFiles() + 1) > MAX_MP4_FILES:
        files = fnmatch.filter(os.listdir("videos/"),"*.mp4")
        for mp4file in files:
            print (mp4file)
            os.remove("videos/"+mp4file)

#new connections handled as separate threads
def on_new_client():
        camera_record()

#tag recorded file with incident stamp
def tag_file():
    print("not implemented yet")
    
#record 10s video and store in videos/
def camera_record():
    with picamera.PiCamera() as camera: # only start camera when we need it.
        camera.resolution = (1280, 720)
        stream = picamera.PiCameraCircularIO(camera, seconds=10)
        #motion_detector = MotionDetector(camera)
        camera.start_recording(stream, format='h264', bitrate=REC_BITRATE,
                intra_period=REC_FRAMERATE)
        print('recording starting...')
        try:
            while True:
                ##camera.split_recording('after.h264')
                time.sleep(10);
                camera.split_recording('after.h264')
                write_before(stream)
                break
        finally:
            print('recording stops...')
            camera.stop_recording()
            reportfilename = "videos/" + getTimeStampedFileName()
            filename=reportfilename+".mp4"
            print(filename)
            removeOldestFile()     
            command = "MP4Box -add {} {}.mp4".format('before.h264',reportfilename)
            try:
                output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
                camera.close() # need to save power    
            except subprocess.CalledProcessError as e:    
                print('failed to convert to mp4')


def listenforInterrupt():
    while True:
        val = GPIO.input(BREAK_PIN)
    if val==1:
        sys.exit()
    time.sleep(0.5)    

def main():
    setupGPIOS()
    _thread.start_new_thread(listenforInterrupt,())
    _thread.start_new_thread(on_new_client,())
    sys.exit()
        
if __name__ == '__main__':
    main()
