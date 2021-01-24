from os import path, environ
from firebase_admin import auth, storage, credentials, initialize_app, firestore

# Load GOOGLE_APPLICATION_CREDENTIALS
key_path = path.join(path.dirname(path.realpath(__file__)), 'edna_service_key.json')
environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

app = initialize_app(credentials.Certificate(environ.get('GOOGLE_APPLICATION_CREDENTIALS')), {
    'storageBucket': 'edna-one.appspot.com'
})

db = firestore.client()