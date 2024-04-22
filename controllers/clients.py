from models.clients import Client,UpdateClient
from exceptions.status_error import CustomHTTPException, InternalServerError
from config.db import db
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from jose import JWTError
import os
from utils.auth import create_access_token, authenticate_user
from bson import ObjectId 
from utils.firebase import upload_image_from_base64
from models.serviceProvider import ServiceProvider,Login,AccessToken
from datetime import datetime, timedelta

class ClientController:
    @staticmethod
    def register_client(client_data):
        name = client_data.get('name')
        email = client_data.get('email')
        password = client_data.get('password')
        image = client_data.get('image')

        if not name:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "name", "message": "Name is required"}])
        if not email:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "email", "message": "Email is required"}])
        if not password or len(password) < 6:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "password", "message": "Password must be at least 6 characters long"}])
        if not image:
            default_image_url = os.getenv("PROFILE_PICTURE")
            if not default_image_url:
                raise InternalServerError("Default image URL is not provided in environment variables")
            image = default_image_url

        if db.get_collection("clients").find_one({"email": email}):
            raise CustomHTTPException(status_code=422, message="Email already exists", error_messages=[{"path": "email", "message": "Email already exists"}])

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(password)

        client = Client(
            name=name,
            email=email,
            password=hashed_password,
            image=image, 
        )

        try:
            db.get_collection("clients").insert_one(client.dict())
            return client
        except Exception as e:
            raise InternalServerError("Failed to register client: " + str(e))
        
    @staticmethod
    def get_client_by_id(client_id):
        try:
            object_id = ObjectId(client_id)
            client = db.get_collection("clients").find_one({"_id": object_id})
            if client:
                client['_id'] = str(client['_id'])

            return client
        except Exception as e:
            raise InternalServerError("Failed to get client: " + str(e))
        
    @staticmethod
    def update_client(client_id: str, client_data: UpdateClient):
        try:
            if not ObjectId.is_valid(client_id):
                raise CustomHTTPException(status_code=400, message="Invalid client ID format", error_messages=[{"path": "provided_id", "message": "Invalid client ID format"}])

            base64_image = client_data.image
            if base64_image:
                image_url = upload_image_from_base64(base64_image, client_id)
                client_data.image = image_url

            if client_data.password:
                password = client_data.password
                if password and len(password) >= 6:
                    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                    hashed_password = pwd_context.hash(password)
                    client_data.password = hashed_password
                else:
                    raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "password", "message": "Password must be at least 6 characters long"}])

            updated_client = db.get_collection("clients").find_one_and_update(
                {"_id": ObjectId(client_id)},
                {"$set": client_data.dict(exclude_unset=True)},
                return_document=True
            )

            if updated_client:
                # Convert ObjectId to string
                updated_client['_id'] = str(updated_client['_id'])
                return updated_client
            else:
                raise HTTPException(status_code=404, detail="Client not found")
        except HTTPException:
            raise
        except Exception as e:
            raise InternalServerError("Failed to update client: " + str(e))
        
#login
        
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class LoginController2:
    @staticmethod
    def login(login_data: Login):
        # email = login_data.email
        # password = login_data.password
        role = login_data.role

        if role != "client":
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "role", "message": "Role must be client"}])

        user = authenticate_user(login_data)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"], "role": user["role"]}, expires_delta=access_token_expires
        )
        return AccessToken(access_token=access_token, token_type="bearer",id=str(user["_id"]))