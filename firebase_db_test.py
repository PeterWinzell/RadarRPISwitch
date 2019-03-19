import firebase_admin, os, sys
from firebase_admin import credentials, firestore, storage, db, auth
from dbutil import FirebaseDbUtility

# get current directory
MAIN_DIR, _ = os.path.split(os.path.abspath(__file__))
PARTITION_NAME = "pics/" # should be added through

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

    
def main():
    # initialize database
    dbutil = FirebaseDbUtility("/damagereport.json", MAIN_DIR)
    # upload file to firebase
    dbutil.uploadBlob('pics/pic0.jpg', "/pics")


if __name__ == '__main__':
    main()
