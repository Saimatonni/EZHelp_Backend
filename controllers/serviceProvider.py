from models.serviceProvider import ServiceProvider,Login,AccessToken,UpdateServiceProviderProfile
from exceptions.status_error import CustomHTTPException, InternalServerError
from config.db import db
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from datetime import datetime, timedelta
import os
from utils.auth import create_access_token, authenticate_user
from bson import ObjectId 
from utils.firebase import upload_image_from_base64
from utils.database import get_user_id_by_email,get_sp_id_by_email
from middleware.validation import validate_access_token


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
        # rating = service_provider_data.get('rating')
        # total_review_count = service_provider_data.get('total_review_count')
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
        if not image:
            default_image_url = os.getenv("PROFILE_PICTURE")
            if not default_image_url:
                raise InternalServerError("Default image URL is not provided in environment variables")
            image = default_image_url
            
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
            # rating=rating,
            # total_review_count=total_review_count,
            image=image,
            role=role,
            password=hashed_password  
        )

        try:
            db.get_collection("service_providers").insert_one(service_provider.dict())
            return service_provider
        except Exception as e:
            raise InternalServerError("Failed to register service provider: " + str(e))
        
 
    @staticmethod
    def get_service_provider_by_id(provider_id):
     try:
        object_id = ObjectId(provider_id)
        service_provider = db.get_collection("service_providers").find_one({"_id": object_id})
        if service_provider:
            service_provider['_id'] = str(service_provider['_id'])

        return service_provider
     except Exception as e:
        raise InternalServerError("Failed to get service provider: " + str(e))
    
    @staticmethod
    def get_all_service_providers():
        try:
            all_service_providers = list(db.get_collection("service_providers").find())
            for provider in all_service_providers:
                provider['_id'] = str(provider['_id'])

            return all_service_providers
        except Exception as e:
            raise InternalServerError("Failed to retrieve all service providers: " + str(e))
        
    @staticmethod
    def update_service_provider(provider_id: str, provider_data: UpdateServiceProviderProfile):
     try:
        if not ObjectId.is_valid(provider_id):
            raise CustomHTTPException(status_code=400, message="Invalid provider ID format", error_messages=[{"path": "provided_id", "message": "Invalid provider ID format"}])

        base64_image = provider_data.pop("image", None)
        if base64_image:
            image_url = upload_image_from_base64(base64_image, provider_id)
            provider_data["image"] = image_url

        # Hash the password if it's provided in the data
        if 'password' in provider_data:
            password = provider_data.pop("password")
            if password and len(password) >= 6:
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                hashed_password = pwd_context.hash(password)
                provider_data["password"] = hashed_password
            else:
                raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "password", "message": "Password must be at least 6 characters long"}])

        updated_provider = db.get_collection("service_providers").find_one_and_update(
            {"_id": ObjectId(provider_id)},
            {"$set": provider_data},
            return_document=True
        )

        if updated_provider:
            # Convert ObjectId to string
            updated_provider['_id'] = str(updated_provider['_id'])
            return updated_provider
        else:
            raise HTTPException(status_code=404, detail="Service provider not found")
     except HTTPException:
        raise
     except Exception as e:
        raise InternalServerError("Failed to update service provider: " + str(e))
    
    @staticmethod
    def assign_service_provider_to_job(job_id: str, provider_id: str, access_token: str):
        try:
            user_email = validate_access_token(access_token)
            user_id = str(get_user_id_by_email(user_email))  
        except HTTPException as e:
            raise CustomHTTPException(status_code=e.status_code, message="Unauthorized", error_messages=[{"path": "access_token", "message": "Invalid or missing access token"}])

        if not user_id:
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "access_token", "message": "User not found"}])
        try:
            object_id = ObjectId(provider_id)
            service_provider = db.get_collection("service_providers").find_one({"_id": object_id})
            if service_provider:
            #    service_provider_dict = dict(service_provider)
               service_provider.pop('_id', None)
            assignment_data = {
                "job_id": job_id,
                "user_id": user_id,
                "provider_details": service_provider
            }
            db.get_collection("assignments").insert_one(dict(assignment_data))

            return assignment_data

        except CustomHTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.message, headers=e.headers)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error", headers={"error_message": str(e)})
        
    @staticmethod
    def get_assignments_for_user(access_token: str):
        try:
            user_email = validate_access_token(access_token)
            user_id = str(get_user_id_by_email(user_email))  
        except HTTPException as e:
            raise CustomHTTPException(status_code=e.status_code, message="Unauthorized", error_messages=[{"path": "access_token", "message": "Invalid or missing access token"}])

        if not user_id:
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "access_token", "message": "User not found"}])

        try:
            assignments = list(db.get_collection("assignments").find({"user_id": user_id}))
            for assignment in assignments:
                assignment['_id'] = str(assignment['_id'])
                assignment['provider_details'].pop('_id', None)

            return assignments

        except Exception as e:
            raise InternalServerError("Failed to retrieve assignments: " + str(e))


        
    


#login

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class LoginController:
    @staticmethod
    def login(login_data: Login):
        user = authenticate_user(login_data)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        return AccessToken(access_token=access_token, token_type="bearer",id=str(user["_id"]))
    
