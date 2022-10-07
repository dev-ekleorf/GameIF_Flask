import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("C:\Users\ekleorf\Documents\gameif-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client() 

