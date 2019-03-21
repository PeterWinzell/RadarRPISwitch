import time
import logging
import os
import fnmatch


class StringFileUtils:
    """ helper class for file and string handling """
    
    logger   = None
    filepath = None
    filext   = None
    
    #initialze with filepath and filextension
    def __init__(self,log,filep,filee):
        self.logger = log
        self.logger.info("initializing StringFileUtils instance")
        self.filepath = filep
        self.filext = filee
        
    #returns a timestamped filename    
    def gettimestampedfilename(self):
        self.logger.info('creating filename getTimeStampedFileName() in StringUtils')
        return time.strftime("report%Y%m%d-%H%M%S")
    
    # count the number files in filepath + fileext
    def countfiles(self):
        return len(fnmatch.filter(os.listdir(self.filepath), "*" + self.filext))
    
    # remove oldest file
    def removeoldestfiles(self, max_files):
        if (self.countfiles() + 1) > max_files:
            files = fnmatch.filter(os.listdir(self.filepath), "*" + self.filext)
            for mp4file in files:
                self.logger.debug('removing: ' + mp4file + ' removeoldestfiles()')
                os.remove(self.filepath+"/"+mp4file)