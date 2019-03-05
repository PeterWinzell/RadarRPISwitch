import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate('damagereport.json')

firebase_admin.initialize_app(cred,{
    'storageBucket':'damagereport-897b3.appspot.com'
    })
db = firestore.client()
bucket = storage.bucket()
blob = bucket.blob('motion-detected.mp4')
file = 'videos/motion-detected.mp4'
with open(file,'rb') as a_file:
    blob.upload_from_file(a_file)
