
import firebase_admin, os, sys
from firebase_admin import credentials, firestore, storage, db, auth


class FirebaseDbUtility:
    """Handles the upload of video files to firebase damagereport-897b3"""
    cred = None
    app = None

    def __init__(self, credfilename,main_dir):
        self.cred = credentials.Certificate(main_dir + credfilename)
        self.app = firebase_admin.initialize_app(self.cred, {
            'storageBucket': 'damagereport-897b3.appspot.com',
            'databaseURL': 'https://damagereport-897b3.firebaseio.com',
            'databaseAuthVariableOverride': {
                'uid': 'qLlrevFUUPhKuVwx7O3hUFRsdUx2'}
        })

    # add a public url to resource such as mp4
    def writeurltodb(self, urlstr):
        root = db.reference()
        root.child('damagereports').push({
            'url': urlstr
        })

    # uploads a blob(video,photo) to firebase
    def uploadBlob(self,filename,partitionstr):
        db = firestore.client()
        bucket = storage.bucket()
        line = filename
        _, _, blobname = line.partition(partitionstr)

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
        self.writeurltodb(urlstr)
