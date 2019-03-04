# version 0.0.1 Peter Winzell jan 2019
import io
import picamera
import time
import picamera.array
import numpy as np
import socket
import subprocess
import fnmatch
import os
import json
import _thread

from getip import get_ip_address # bind to server address
from PIL import Image, ImageDraw

prior_image = None
camera = None

REC_RESOLUTION = (1280, 720) # the recording resolution
REC_FRAMERATE = 24           # the recording framerate
REC_SECONDS = 10             # number of seconds to store in ring buffer
REC_BITRATE = 1000000        # bitrate for H.264 encoder

MOTION_MAGNITUDE = 60        # the magnitude of vectors required for motion
MOTION_VECTORS = 10          # the number of vectors required to detect motion

MAX_MP4_FILES = 4            # the maximum number of files we are allowed to store



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
    #return time.strftime("report%Y%m%d-%H%M%S")
    return "motion-detected"

def numFiles():
    return len(fnmatch.filter(os.listdir("videos/"),"*.mp4"))
    
def removeOldestFile():
    if (numFiles() + 1) > MAX_MP4_FILES:
        files = fnmatch.filter(os.listdir("videos/","*.mp4"))
        for mp4file in files:
            print (mp4file)                           

#new connections handled as separate threads
def on_new_client(clientsocket,addr):
    while True:
        jsoncommandStr = clientsocket.recv(1024)
        if not jsoncommandStr:
            break;
        #try:
        commandJSON = json.loads(jsoncommandStr.decode())
        commandstring = commandJSON["command"]
        print(commandstring)
        if   (commandstring == 'motion'):
            print("is here")
            camera_record()
        elif (commandstring == 'incident'):
            tag_file()
        else:
            continue    
        #except Exception as e:
         #   print(e)
        print ("command:   " + commandJSON["command"])
        print ("cameraId:  " + repr(commandJSON["cameraId"]))
        print ("timestamp: " + repr(commandJSON["timestamp"]))
    clientsocket.close()

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
            if os.path.exists(reportfilename):
                os.remove(reportfilename)
            else:
                print("could not remove previous file")       
            command = "MP4Box -add {} {}.mp4".format('before.h264',reportfilename)
            try:
                output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
                camera.close() # need to save power    
            except subprocess.CalledProcessError as e:    
                print('failed to convert to mp4') 
     
def main():
    
    # setup socket server
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    host = "10.242.179.156" #get_ip_address()
    port = 49152
    
    s.bind((host,port))
    s.listen(5)
    
    while True:
        # wait for a connection which we use as trigger to start a 10s recording
        print('waiting for connection...')
        c,addr = s.accept() 
        #wait for command from client
        
        _thread.start_new_thread(on_new_client,(c,addr))
        
        # setup and start camera recording
        # removeOldestFile()                       
        #stream = picamera.PiCameraCircularIO(camera, seconds=10)
       # motion_detector = MotionDetector(camera)
       # camera.start_recording(
        #        stream, format='h264', bitrate=REC_BITRATE,
         #       intra_period=REC_FRAMERATE)

        #print('recording starting...')
        #try:
          #  while True:
                ##camera.split_recording('after.h264')
           #     time.sleep(10);
            #    camera.split_recording('after.h264')
             #   write_before(stream)
              #  break
       # finally:
        #    print('recording stops...')
         #   camera.stop_recording()
          #  reportfilename = "videos/" + getTimeStampedFileName()
           # command = "MP4Box -add {} {}.mp4".format('before.h264',reportfilename)
            #try:
             #   output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
           # except subprocess.CalledProcessError as e:    
             #   print('failed to convert to mp4')    


if __name__ == '__main__':
    #with picamera.PiCamera() as camera:
        #camera.resolution = (1280, 720)
        #main(camera)
    main()
