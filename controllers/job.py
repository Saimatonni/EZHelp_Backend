from models.job import Job
from exceptions.status_error import CustomHTTPException, InternalServerError
from config.db import db
from utils.firebase import upload_image_from_base64
from bson import ObjectId
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
import os
from middleware.validation import validate_access_token
from utils.database import get_user_id_by_email,get_sp_id_by_email

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
        open = job_data.get('open')
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
                
            job_data['bidded_sp_ids'] = []
            
            job = Job(
                userId=user_id,
                workType=work_type,
                address=address,
                GPSCoordinates=gps_coordinates,
                emergency=emergency,
                open=open,
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
        
    @staticmethod
    def bid_on_job(job_id: ObjectId, sp_id: str, access_token: str):
        try:
            sp_mail = validate_access_token(access_token)
            sp_id = str(get_sp_id_by_email(sp_mail))
        except HTTPException as e:
            raise CustomHTTPException(status_code=e.status_code, message="Unauthorized", error_messages=[{"path": "access_token", "message": "Invalid or missing access token"}])

        if not sp_id:
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "access_token", "message": "User not found"}])

        try:
            job = db.get_collection("jobs").find_one({"_id": job_id})
            if not job:
                raise CustomHTTPException(status_code=404, message="Job not found", error_messages=[{"path": "job_id", "message": "Job with the provided ID does not exist"}])

            db.get_collection("jobs").update_one({"_id": job_id}, {"$addToSet": {"bidded_sp_ids": sp_id}})
            
            return {"message": "Service provider bid successfully added to the job", "job_id": str(job_id)}

        except Exception as e:
            raise InternalServerError("Failed to bid on the job: " + str(e))
        
    @staticmethod
    def get_jobs_by_sp_id(sp_id: str, access_token: str):
        try:
            sp_mail = validate_access_token(access_token)
            vsp_id = str(get_sp_id_by_email(sp_mail))
        except HTTPException as e:
            raise CustomHTTPException(status_code=e.status_code, message="Unauthorized", error_messages=[{"path": "access_token", "message": "Invalid or missing access token"}])

        if not vsp_id:
            raise CustomHTTPException(status_code=401, message="Unauthorized", error_messages=[{"path": "access_token", "message": "User not found"}])
        try:
            jobs = list(db.get_collection("jobs").find({"bidded_sp_ids": sp_id}))
            for job in jobs:
                job['_id'] = str(job['_id'])
            return jobs

        except Exception as e:
            raise InternalServerError("Failed to retrieve jobs by service provider ID: " + str(e))
        
    @staticmethod
    def get_service_providers_by_job_id(job_id: str):
        try:
            job_id_obj = ObjectId(job_id)
            job = db.get_collection("jobs").find_one({"_id": job_id_obj})
            if not job:
                raise CustomHTTPException(status_code=404, message="Job not found", error_messages=[{"path": "job_id", "message": "Job with the provided ID does not exist"}])
            
            bidded_sp_ids = job.get("bidded_sp_ids", [])
            service_providers = []
            for sp_id in bidded_sp_ids:
                object_id = ObjectId(sp_id)
                service_provider = db.get_collection("service_providers").find_one({"_id": object_id})
                if service_provider:
                    service_provider['_id'] = str(service_provider['_id'])
                if service_provider:
                    service_providers.append(service_provider)
            return service_providers
        except Exception as e:
            raise InternalServerError("Failed to retrieve service providers details: " + str(e))
        
    @staticmethod
    def update_job_open_status(job_id: str, access_token: str, open_status: bool):
        try:
            user_email = validate_access_token(access_token)
            user_id = str(get_user_id_by_email(user_email))
        except HTTPException as e:
            raise CustomHTTPException(status_code=e.status_code, message="Unauthorized",
                                      error_messages=[{"path": "access_token",
                                                       "message": "Invalid or missing access token"}])

        if not user_id:
            raise CustomHTTPException(status_code=401, message="Unauthorized",
                                      error_messages=[{"path": "access_token", "message": "User not found"}])

        try:
            job_id_obj = ObjectId(job_id)
            job = db.get_collection("jobs").find_one({"_id": job_id_obj})

            if not job:
                raise CustomHTTPException(status_code=404, message="Job not found",
                                          error_messages=[{"path": "job_id",
                                                           "message": "Job with the provided ID does not exist"}])

            db.get_collection("jobs").update_one({"_id": job_id_obj}, {"$set": {"open": open_status}})

            return {"message": "Job open status updated successfully", "job_id": str(job_id)}

        except Exception as e:
            raise InternalServerError("Failed to update job open status: " + str(e))
