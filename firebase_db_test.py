import firebase_admin, os, sys
from firebase_admin import credentials, firestore, storage, db, auth

# get current directory
MAIN_DIR, _ = os.path.split(os.path.abspath(__file__))
PARTITION_NAME = "pics/" # should be added through
CREDFILENAME = ""

class FirebaseDbUtility:
    """Handles the upload of video files to firebase"""
    cred = None
    app = None

    def __init__(self, credfilename):
        self.cred = credentials.Certificate(MAIN_DIR + credfilename)
        self.app = firebase_admin.initialize_app(self.cred, {
            'storageBucket': 'damagereport-897b3.appspot.com',
            'databaseURL': 'https://damagereport-897b3.firebaseio.com',
            'databaseAuthVariableOverride': {
                'uid': 'qLlrevFUUPhKuVwx7O3hUFRsdUx2'} 
        })

    def writeurltoB(self, urlstr):
        root = db.reference()
        root.child('damagereports').push({
            'url': urlstr
        })

    def uploadBlob(self,filename):
        db = firestore.client()
        bucket = storage.bucket()
        line = filename
        _, _, blobname = line.partition(PARTITION_NAME)

        blob = bucket.blob("damagereport/" + blobname)
        print("Blob path is : " + blob.path)
        filepath = filename

        # blob.make_public()
        with open(filepath, 'rb') as a_file:
            blob.upload_from_file(a_file)

        # let the files be public available
        blob.make_public()
        print("url : " + blob.public_url)
        urlstr = blob.public_url
        writeURLtoDB(urlstr)



# connect to firebase db
def iniateDbConnection2():
    print(MAIN_DIR)
    cred = credentials.Certificate(MAIN_DIR + '/damagereport.json')
    # logger.debug('cred iniateDbConnection()')
    app = firebase_admin.initialize_app(cred, {
        'storageBucket': 'damagereport-897b3.appspot.com',
        'databaseURL': 'https://damagereport-897b3.firebaseio.com',
        'databaseAuthVariableOverride': {
            'uid': 'qLlrevFUUPhKuVwx7O3hUFRsdUx2'}
    }
                                        )


# connect to firebase db
def iniateDbConnection():
    cred = credentials.Certificate(MAIN_DIR + 'damagereport.json')
    # logger.debug('cred iniateDbConnection()')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'damagereport-897b3.appspot.com'
    })


#
urlstr2 = "https://storage.googleapis.com/damagereport-897b3.appspot.com/report20190313-151722.mp4"


def uploadBlobFile(filename):
    db = firestore.client()
    bucket = storage.bucket()
    line = filename
    _, _, blobname = line.partition("pics/")

    blob = bucket.blob("damagereport/" + blobname)
    print("Blob oath is : " + blob.path)
    filepath = filename

    # blob.make_public()
    with open(filepath, 'rb') as a_file:
        blob.upload_from_file(a_file)

    # let the files be public available
    blob.make_public()
    print("url : " + blob.public_url)
    urlstr = blob.public_url
    writeURLtoDB(urlstr)


def writeURLtoDB(urlstr):
    root = db.reference()
    root.child('damagereports').push({
        'url': urlstr
    })


def downLoadBlob():
    print(" downloading... ")


def main():
    # initialize database
    dbutil = FirebaseDbUtility("/damagereport.json")
    # upload file to firebase
    dbutil.uploadBlob('pics/pic0.jpg')


if __name__ == '__main__':
    main()
