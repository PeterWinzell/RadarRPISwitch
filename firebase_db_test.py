import firebase_admin
from firebase_admin import credentials, firestore, storage, db

MAIN_DIR = "/home/pi/radar-sensor/RadarRPISwitch/"

# connect to firebase db 
def iniateDbConnection2():
    cred = credentials.Certificate(MAIN_DIR+'damagereport.json')
    #logger.debug('cred iniateDbConnection()')
    firebase_admin.initialize_app(cred,{
         'storageBucket':'damagereport-897b3.appspot.com',
          'databaseURL':'https://damagereport-897b3.firebaseio.com'
    })
    
# connect to firebase db 
def iniateDbConnection():
    cred = credentials.Certificate(MAIN_DIR+'damagereport.json')
    #logger.debug('cred iniateDbConnection()')
    firebase_admin.initialize_app(cred,{
        'storageBucket':'damagereport-897b3.appspot.com'
    })     
    
#
urlstr =  "https://storage.googleapis.com/damagereport-897b3.appspot.com/report20190313-151722.mp4"
 
def writeURLtoDB():
    root = db.reference()
    new_url = root.child('damagereports').push({
        'url':urlstr
    })
    
def copy
    
def main():
    iniateDbConnection2()
    writeURLtoDB()

if __name__ == '__main__':
    main()
    
