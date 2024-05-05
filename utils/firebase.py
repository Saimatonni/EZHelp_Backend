import pyrebase
import base64

class InternalServerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# Initialize Firebase with your config
firebaseConfig = {
    "apiKey": "AIzaSyDB7TkrfABtiG2U90SEDY8OrIePK70n93Y",
    "authDomain": "ezhelp-1f1fd.firebaseapp.com",
    "projectId": "ezhelp-1f1fd",
    "storageBucket": "ezhelp-1f1fd.appspot.com",
    "messagingSenderId": "1040025544772",
    "appId": "1:1040025544772:web:b338f13096778b9ba0b411",
    "measurementId": "G-XZH9WY8H46",
    "databaseURL": "https://programmingquiz-1054f-default-rtdb.firebaseio.com/",
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


def upload_image_from_base64(base64_image, provider_id):
        try:
       
            image_data = base64.b64decode(base64_image)

         
            filename = f"images/{provider_id}.jpg" 

         
            storage.child(filename).put(image_data)

            image_url = storage.child(filename).get_url(None)

            return image_url
        except Exception as e:
            raise InternalServerError("Failed to upload image: " + str(e))
