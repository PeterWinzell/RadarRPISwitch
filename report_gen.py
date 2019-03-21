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
import firebase_admin
import sys,traceback
import logging
from connection import has_internetconnection
from firebase_admin import credentials, firestore, storage, db
from PIL import Image, ImageDraw

from dbutil import FirebaseDbUtility
from stringutils import StringFileUtils

prior_image = None
camera = None

REC_RESOLUTION = (1280, 720) # the recording resolution
REC_FRAMERATE = 24           # the recording framerate
REC_SECONDS = 10             # number of seconds to store in ring buffer
REC_BITRATE = 1000000        # bitrate for H.264 encoder

MOTION_MAGNITUDE = 60        # the magnitude of vectors required for motion
MOTION_VECTORS = 10          # the number of vectors required to detect motion

MAX_MP4_FILES = 0           # the maximum number of files we are allowed to store
                    
SHUT_PIN  = 5                # Set this pin to low when we want the pi to turn off power.


MAIN_DIR = "/home/pi/radar-sensor/RadarRPISwitch/"
FILE_EXT = ".mp4"
logger = logging.getLogger('report_gen_logger')

SHUTDOWN = True

def setupLogging():   
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(MAIN_DIR +'report.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    
def setupGPIOS():
    logger.info('setting up GPIO pins setupGPIOS()')
    global SHUT_PIN
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SHUT_PIN,GPIO.OUT)
    GPIO.output(SHUT_PIN,GPIO.HIGH)

def write_before(stream):
    # Write the entire content of the circular buffer to disk. No need to lock
    # the stream here as we're definitely not writing to it simultaneously
    logger.info('writing buffer to stream write_before(stream)')
    with io.open(MAIN_DIR + 'before.h264', 'wb') as output:
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

#def getTimeStampedFileName():
#    logger.info('creating filename getTimeStampedFileName()')
#    return time.strftime("report%Y%m%d-%H%M%S")
    #return "motion-detected"

#def numFiles():
#   return len(fnmatch.filter(os.listdir(MAIN_DIR + "videos/"),"*.mp4"))

# remove all previous mp4 files 
#def removeOldestFile():
#    if (numFiles() + 1) > MAX_MP4_FILES:
#        files = fnmatch.filter(os.listdir(MAIN_DIR+"videos/"),"*.mp4")
#        for mp4file in files:
#            logger.debug('removing: ' + mp4file + ' removeOldestFile()')
#            os.remove(MAIN_DIR +"videos/"+mp4file)

#new connections handled as separate threads
def on_new_client(db):
        #global SHUTDOWN
        try:
            camera_record(db)
        except  Exception as e:
            #errstr = traceback.format_exc()
            logger.debug(str(e) + ' on_new_client()')
        finally:    
            if SHUTDOWN == False:
                logger.debug(' shutdown process canceled by user on_new_client()')
                sys.exit()
            else:
                start_pi_shutdown()

#tag recorded file with incident stamp
#def tag_file():
#    logger.info("not implemented yet tag_file()")
    
#record 10s video and store in videos/
def camera_record(db):
    stringutils = StringFileUtils(logger, MAIN_DIR + "/videos", FILE_EXT)
    logger.info(' accessing camera')
    with picamera.PiCamera() as camera: # only start camera when we need it.
        camera.resolution = (800, 600)
        stream = picamera.PiCameraCircularIO(camera, seconds=10)
        #motion_detector = MotionDetector(camera)
        #camera.start_preview()
        camera.start_recording(stream, format='h264', bitrate=REC_BITRATE,
                intra_period=REC_FRAMERATE)
        logger.debug('recording starting... camera_record() format h264 800x600')
        try:
            while True:
                ##camera.split_recording('after.h264')
                time.sleep(10);
                camera.split_recording(MAIN_DIR + 'after.h264')
                write_before(stream)
                break
        except Exception as e:
            logger.debug(' camera loop error ' + str(e))
        finally:
            
            logger.debug('recording stops...camera_record()')
            camera.stop_recording()
            #camera.stop_preview()
            camera.close()
            logger.debug('camera closed...camera_record()')
            
        reportfilename = MAIN_DIR + "videos/" + stringutils.gettimestampedfilename()
        filename=reportfilename + FILE_EXT
        logger.debug('report filename is ' + filename + ' camera_record()')
        stringutils.removeoldestfiles(MAX_MP4_FILES)
            
        command = "MP4Box -add {} {}.mp4".format(MAIN_DIR +'before.h264',reportfilename)
        logger.debug('converting to mp4 camera_record()')
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
        db.uploadblob(reportfilename + FILE_EXT, "videos/")
            
            

#def listenforInterrupt():
#    global SHUTDOWN
#    try:
#        while SHUTDOWN == True:
#            val = GPIO.input(BREAK_PIN)
#            if val==1:
#                print(' breaking shutdown sequence...')
#                SHUTDOWN = False
#                break
#            time.sleep(0.5)
#    except Exception as e: print(e)
    
 
# connect to firebase db 
#def iniateDbConnection():
#    cred = credentials.Certificate(MAIN_DIR+'damagereport.json')
#    logger.debug('cred iniateDbConnection()')
#    firebase_admin.initialize_app(cred,{
#        'storageBucket':'damagereport-897b3.appspot.com',
#        'databaseURL':'https://damagereport-897b3.firebaseio.com'
#    })

#def addUrlToDB(urlstr):
#    root = db.reference()
#    new_url = root.child('damagereports').push({
#        'url':urlstr
#    })
#    logger.debug(urlstr + ' added to db')
    
#upload video to cloud    
#def sendToCloud(filename):   
#    db = firestore.client()
#    bucket = storage.bucket()
#    line = filename
#    _,_,blobname = line.partition("videos/")
#    logger.debug('blobname is '+ blobname + ' sendToCloud()')
#    blob = bucket.blob(blobname)
#    filepath = filename
#    logger.debug('filepath is: ' + filepath + ' sendToCloud()')
#    with open(filepath,'rb') as a_file:
#        blob.upload_from_file(a_file)    
#    logger.debug("video access URL is: " + blob.public_url + " sendToCloud(filename) ")
#    #addUrlToDB(blob.public_url)
   
    #root = db.reference()
    #root.child('damagereport').push({
    #    'url':blob.public_url
    #})
    
# setting  
def start_pi_shutdown():
    logger.debug(' stop cycle ******')
    GPIO.output(SHUT_PIN,GPIO.LOW)
    subprocess.call(['shutdown','-h','now'],shell=False)

def handle_exception(exc_type, exc_value, exc_traceback):
    logger.debug(str.join( "exception: ", traceback.format_exception(exc_type,exc_value,exc_traceback )))
    #sys.exit(1)
    
def main():
    setupLogging()
    sys.excepthook = handle_exception
    logger.info('start cycle ***** ')
    if has_internetconnection(logger) == False:
        SHUTDOWN = False
        logger.debug("exiting script no internet connection main()")
        sys.exit()
    setupGPIOS()
    db = FirebaseDbUtility("damagereport.json",MAIN_DIR, logger)
    #_thread.start_new_thread(listenforInterrupt,())
    #_thread.start_new_thread(on_new_client,())
    on_new_client(db)
        
if __name__ == '__main__':
    main()
