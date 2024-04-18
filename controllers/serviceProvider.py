from models.serviceProvider import ServiceProvider,Login,AccessToken
from exceptions.status_error import CustomHTTPException, InternalServerError
from config.db import db
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

class ServiceProviderController:
    @staticmethod
    def register_service_provider(service_provider_data):
        name = service_provider_data.get('name')
        work_type = service_provider_data.get('work_type')
        pay_per_hour = service_provider_data.get('pay_per_hour')
        experience = service_provider_data.get('experience')
        email = service_provider_data.get('email')
        phone_number = service_provider_data.get('phone_number')
        nid_number = service_provider_data.get('nid_number')
        rating = service_provider_data.get('rating')
        total_review_count = service_provider_data.get('total_review_count')
        image = service_provider_data.get('image')
        password = service_provider_data.get('password')

        role = "serviceprovider"

        if not name:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "name", "message": "Name is required"}])
        if not work_type:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "work_type", "message": "Work type is required"}])
        if not pay_per_hour:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "pay_per_hour", "message": "Pay per hour is required"}])
        if not experience:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "experience", "message": "Experience is required"}])
        if not email:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "email", "message": "Email is required"}])
        if not phone_number:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "phone_number", "message": "Phone number is required"}])
        if not nid_number:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "nid_number", "message": "NID number is required"}])
        if not password or len(password) < 6:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "password", "message": "Password must be at least 6 characters long"}])

        if db.get_collection("service_providers").find_one({"email": email}):
            raise CustomHTTPException(status_code=422, message="Email already exists", error_messages=[{"path": "email", "message": "Email already exists"}])

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(password)

        service_provider = ServiceProvider(
            name=name,
            work_type=work_type,
            pay_per_hour=pay_per_hour,
            experience=experience,
            email=email,
            phone_number=phone_number,
            nid_number=nid_number,
            rating=rating,
            total_review_count=total_review_count,
            image=image,
            role=role,
            password=hashed_password  
        )

        try:
            db.get_collection("service_providers").insert_one(service_provider.dict())
            return service_provider
        except Exception as e:
            raise InternalServerError("Failed to register service provider: " + str(e))


#login
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginController:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def authenticate_user(login_data: Login):
        user = db.get_collection("service_providers").find_one({"email": login_data.email})
        if not user:
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "email", "message": "Email not found"}])
        if not pwd_context.verify(login_data.password, user["password"]):
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "password", "message": "Incorrect password"}])
        return user

    @staticmethod
    def login(login_data: Login):
        user = LoginController.authenticate_user(login_data)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = LoginController.create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        return AccessToken(access_token=access_token, token_type="bearer")