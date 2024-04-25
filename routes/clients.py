from fastapi import APIRouter, HTTPException, Header
from controllers.clients import ClientController,LoginController2
from exceptions.status_error import CustomHTTPException
from models.clients import Client,UpdateClient
from middleware.validation import validate_access_token
from models.serviceProvider import ServiceProvider,Login

client_router = APIRouter()

@client_router.post("/clients/register")
async def register_client(client_data: Client):
        client = ClientController.register_client(client_data.dict())
        return {"message": "Client registered successfully", "data": client}

@client_router.post("/clients/login")
async def login(login_data: Login):
    try:
        access_token = LoginController2.login(login_data)
        return {
            "message": "Login successful",
            "access_token": access_token.access_token,
            "token_type": access_token.token_type,
            "client_id": access_token.id
        }
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@client_router.get("/clients/{client_id}")
async def get_client(client_id: str, access_token: str = Header(..., description="Access Token")):
    try:
        user_email = validate_access_token(access_token)
        client = ClientController.get_client_by_id(client_id)

        if client is None:
            raise HTTPException(status_code=404, detail="Client not found")

        return {"message": "Client details retrieved successfully", "data": client}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@client_router.put("/clients/{client_id}")
async def update_client(client_id: str, client_data: UpdateClient, access_token: str = Header(..., description="Access Token")):
    try:
        user_email = validate_access_token(access_token)
        updated_client = ClientController.update_client(client_id, client_data)
        return {"message": "Client updated successfully", "data": updated_client}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
