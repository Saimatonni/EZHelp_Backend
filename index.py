from fastapi import FastAPI
from routes.serviceProviders import serviceProvider
from routes.clients import client_router
app = FastAPI()
app.include_router(serviceProvider)
app.include_router(client_router)
