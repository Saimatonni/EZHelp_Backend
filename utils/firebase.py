import pyrebase
import base64
from fastapi import HTTPException
import binascii
import os 
from dotenv import load_dotenv


# Initialize Firebase
config = {
  "apiKey": "AIzaSyDB7TkrfABtiG2U90SEDY8OrIePK70n93Y",
  "authDomain": "ezhelp-1f1fd.firebaseapp.com",
  "projectId": "ezhelp-1f1fd",
  "storageBucket": "ezhelp-1f1fd.appspot.com",
  "messagingSenderId": "1040025544772",
  "appId": "1:1040025544772:web:b338f13096778b9ba0b411",
  "measurementId": "G-XZH9WY8H46"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# Function to upload image
def upload_image_from_base64(base64_string:str, userId:int):
    try:
        # Decode base64 string to bytes
        image_bytes = base64.b64decode(base64_string)
        
        # You may want to specify a filename here or generate one dynamically
        filename = f"{userId}.jpg"
        
        # Upload image to Firebase Storage
        storage.child("images/" + filename).put(image_bytes)
        
        # Get URL of the uploaded image
        url = storage.child("images/" + filename).get_url(None)
        
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
