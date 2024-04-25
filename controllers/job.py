from models.job import Job
from exceptions.status_error import CustomHTTPException, InternalServerError
from config.db import db
from utils.firebase import upload_image_from_base64
from bson import ObjectId
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
import os
from jose import jwt, JWTError
from middleware.validation import validate_access_token
from utils.database import get_user_id_by_email

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

class JobController:
    @staticmethod
    def create_job(job_data, access_token):
        try:
            user_email = validate_access_token(access_token)
            user_id = str(get_user_id_by_email(user_email))  
        except HTTPException as e:
            raise CustomHTTPException(status_code=e.status_code, message="Unauthorized", error_messages=[{"path": "access_token", "message": "Invalid or missing access token"}])

        if not user_id:
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "access_token", "message": "User not found"}])

        work_type = job_data.get('workType')
        address = job_data.get('address')
        gps_coordinates = job_data.get('GPSCoordinates')
        emergency = job_data.get('emergency')
        pay_amount = job_data.get('payAmount')
        short_title = job_data.get('shortTitle')
        description = job_data.get('description')
        images = job_data.get('images')
        start_date = job_data.get('startDate')
        end_date = job_data.get('endDate')

        if not work_type:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "workType", "message": "Work type is required"}])
        if not address:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "address", "message": "Address is required"}])
        if not gps_coordinates:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "GPSCoordinates", "message": "GPS coordinates are required"}])
        if not emergency:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "emergency", "message": "Emergency flag is required"}])
        if not pay_amount:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "payAmount", "message": "Pay amount is required"}])
        if not short_title:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "shortTitle", "message": "Short title is required"}])
        if not description:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "description", "message": "Description is required"}])
        if not images:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "images", "message": "Images are required"}])
        if not start_date:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "startDate", "message": "Start date is required"}])
        if not end_date:
            raise CustomHTTPException(status_code=400, message="Bad Request", error_messages=[{"path": "endDate", "message": "End date is required"}])

        try:
            uploaded_image_urls = []
            for image in images:
                image_url = upload_image_from_base64(image, user_id)
                uploaded_image_urls.append(image_url)
            
            job = Job(
                userId=user_id,
                workType=work_type,
                address=address,
                GPSCoordinates=gps_coordinates,
                emergency=emergency,
                payAmount=pay_amount,
                shortTitle=short_title,
                description=description,
                images=uploaded_image_urls,
                startDate=start_date,
                endDate=end_date
            )

            db.get_collection("jobs").insert_one(job.dict())
            return job
        except Exception as e:
            raise InternalServerError("Failed to create job: " + str(e))
        
    @staticmethod
    def get_all_jobs():
     try:
        all_jobs = list(db.get_collection("jobs").find())
        for job in all_jobs:
            job['_id'] = str(job['_id'])

        return all_jobs
     except Exception as e:
        raise InternalServerError("Failed to retrieve all jobs: " + str(e))
    
    @staticmethod
    def get_job_by_id(job_id: ObjectId):
      try:
        job = db.get_collection("jobs").find_one({"_id": job_id})
        if job:
            job['_id'] = str(job['_id'])
            return job
        else:
            raise CustomHTTPException(status_code=404, message="Job not found", error_messages=[{"path": "job_id", "message": "Job with the provided ID does not exist"}])
      except Exception as e:
        raise InternalServerError("Failed to retrieve job details: " + str(e))
    
    @staticmethod
    def get_jobs_by_user_id(user_id: str):
        try:
            jobs = list(db.get_collection("jobs").find({"userId": user_id}))
            for job in jobs:
                job['_id'] = str(job['_id'])
            return jobs
        except Exception as e:
            raise InternalServerError("Failed to retrieve jobs by user ID: " + str(e))
        
    @staticmethod
    def delete_job(job_id: ObjectId):
        try:
            result = db.get_collection("jobs").delete_one({"_id": job_id})
            if result.deleted_count == 0:
                raise InternalServerError("Failed to delete job: Job not found")

        except Exception as e:
            raise InternalServerError("Failed to delete job: " + str(e))
