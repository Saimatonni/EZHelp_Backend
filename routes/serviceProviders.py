from fastapi import APIRouter, HTTPException
from controllers.serviceProvider import ServiceProviderController,LoginController
from exceptions.status_error import BadRequest, UnprocessableEntity, InternalServerError
from models.serviceProvider import ServiceProvider,Login,AccessToken

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




