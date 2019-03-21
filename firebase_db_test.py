import firebase_admin, os, sys
from firebase_admin import credentials, firestore, storage, db, auth
from dbutil import FirebaseDbUtility

# get current directory
MAIN_DIR, _ = os.path.split(os.path.abspath(__file__))
PARTITION_NAME = "pics/" # should be added through
 
  
def main():
    # initialize database
    dbutil = FirebaseDbUtility("/damagereport.json", MAIN_DIR)
    # upload file to firebase
    dbutil.uploadBlob('pics/pic0.jpg', "/pics")


if __name__ == '__main__':
    main()
