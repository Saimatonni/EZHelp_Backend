from fastapi import APIRouter, HTTPException, Header
from controllers.job import JobController
from exceptions.status_error import CustomHTTPException
from models.job import Job
from middleware.validation import validate_access_token
from bson import ObjectId
from utils.database import get_user_id_by_email

job_router = APIRouter()

@job_router.post("/jobs/create")
async def create_job(job_data: Job, access_token: str = Header(..., description="Access Token")):
    try:
        job = JobController.create_job(job_data.dict(), access_token)
        return {"message": "Job created successfully", "data": job}
    except CustomHTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message, headers=e.headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error", headers={"error_message": str(e)})
    
@job_router.get("/jobs")
async def get_all_jobs():
    try:
        all_jobs = JobController.get_all_jobs()
        return {"message": "All jobs retrieved successfully", "data": all_jobs}
    except Exception  as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@job_router.get("/jobs/{job_id}")
async def get_job_by_id(job_id: str):
    try:
        job_id_obj = ObjectId(job_id)
        job = JobController.get_job_by_id(job_id_obj)
        return {"message": "Job details retrieved successfully", "data": job}
    except CustomHTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message, headers=e.headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error", headers={"error_message": str(e)})
    
    
@job_router.get("/jobs/user/{user_id}")
async def get_jobs_by_user_id(user_id: str, access_token: str = Header(..., description="Access Token")):
    try:
        user_email = validate_access_token(access_token)
        validated_user_id = get_user_id_by_email(user_email)
        if user_id != str(validated_user_id):
            raise CustomHTTPException(status_code=403, message="Forbidden", error_messages=[{"path": "user_id", "message": "You are not authorized to access jobs for this user"}])
        jobs = JobController.get_jobs_by_user_id(user_id)
        return {"message": "Jobs retrieved successfully", "data": jobs}
    except CustomHTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message, headers=e.headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error", headers={"error_message": str(e)})
    
    
@job_router.delete("/jobs/delete")
async def delete_job(job_id: str, access_token: str = Header(..., description="Access Token")):
    try:
        validate_access_token(access_token)
        job_id_obj = ObjectId(job_id)
        JobController.delete_job(job_id_obj)
        return {"message": "Job deleted successfully"}
    except CustomHTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message, headers=e.headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error", headers={"error_message": str(e)})