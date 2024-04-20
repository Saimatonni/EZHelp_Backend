from fastapi import APIRouter, HTTPException, Header
from controllers.serviceProvider import ServiceProviderController,LoginController
from exceptions.status_error import BadRequest, UnprocessableEntity, InternalServerError
from models.serviceProvider import ServiceProvider,Login,AccessToken
from middleware.validation import validate_access_token
from config.db import db
import collections


serviceProvider = APIRouter()

@serviceProvider.post("/service-providers/register")
async def register_service_provider(service_provider_data: ServiceProvider):
    service_provider = ServiceProviderController.register_service_provider(service_provider_data.dict())
    return {"message": "Service provider registered successfully", "data": service_provider}


@serviceProvider.post("/service-providers/login")
async def login(login_data: Login):
    try:
        access_token = LoginController.login(login_data)
        return {
            "message": "Login successful",
            "access_token": access_token.access_token,
            "token_type": access_token.token_type
        }
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@serviceProvider.get("/service-providers/{provider_id}")
async def get_service_provider(provider_id: str, access_token: str = Header(..., description="Access Token")):
    try:
        user_email = validate_access_token(access_token)
        service_provider = ServiceProviderController.get_service_provider_by_id(provider_id)

        if service_provider is None:
            raise HTTPException(status_code=404, detail="Service provider not found")

        return {"message": "Service provider details retrieved successfully", "data": service_provider}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@serviceProvider.get("/service-providers")
async def get_all_service_providers():
    try:
        service_providers = ServiceProviderController.get_all_service_providers()
        return {"message": "All service providers retrieved successfully", "data": service_providers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# @serviceProvider.put("/service-providers/{provider_id}")
# async def update_service_provider(provider_id: str, provider_data: ServiceProvider, access_token: str = Header(..., description="Access Token")):
#     try:
#         user_email = validate_access_token(access_token)
#         updated_provider = ServiceProviderController.update_service_provider(provider_id, provider_data.dict())
#         return {"message": "Service provider updated successfully", "data": updated_provider}
#     except HTTPException as http_exception:
#         raise http_exception
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))