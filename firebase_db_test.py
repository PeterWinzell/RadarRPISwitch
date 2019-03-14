import firebase_admin, os, sys
from firebase_admin import credentials, firestore, storage, db

#get current directory
MAIN_DIR,_ = os.path.split(os.path.abspath(__file__))

# connect to firebase db 
def iniateDbConnection2():
    print(MAIN_DIR)
    cred = credentials.Certificate(MAIN_DIR+'/damagereport.json')
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

def uploadBlobFile(filename):
        db = firestore.client()
        bucket = storage.bucket()
        line = filename
        _, _, blobname = line.partition("pics/")


        blob = bucket.blob("damagereport/" + blobname)
        print("Blob oath is : " + blob.path)
        filepath = filename

        #blob.make_public()
        with open(filepath, 'rb') as a_file:
            blob.upload_from_file(a_file)

        # let the files be public available
        blob.make_public()
        print("url : " + blob.public_url )
...


def writeURLtoDB():
    root = db.reference()
    new_url = root.child('damagereports').push({
        'url':urlstr
    })


def downLoadBlob():
    print(" downloading... ")

    
def main():
    iniateDbConnection2()
    #writeURLtoDB()
    uploadBlobFile(MAIN_DIR + '/pics/pic0.jpg')

if __name__ == '__main__':
    main()
    
