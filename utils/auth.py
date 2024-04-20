# auth.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from exceptions.status_error import CustomHTTPException
from config.db import db
from models.serviceProvider import Login,AccessToken
import os
from fastapi import HTTPException, Depends
from jose import JWTError, jwt

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
        return encoded_jwt


def authenticate_user(login_data: Login):
        user = db.get_collection("service_providers").find_one({"email": login_data.email})
        if not user:
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "email", "message": "Email not found"}])
        if not pwd_context.verify(login_data.password, user["password"]):
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "password", "message": "Incorrect password"}])
        return user