import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("vacaition-8be20-78cb438c854f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
collection = db.collection('data')

def getUserInfo(u_id: str):
    doc = collection.document('sampledoc')
    return doc.get().to_dict()