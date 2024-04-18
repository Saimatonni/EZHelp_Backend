from fastapi import FastAPI
from routes.serviceProviders import serviceProvider
app = FastAPI()
app.include_router(serviceProvider)

