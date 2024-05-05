from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.serviceProviders import serviceProvider
from routes.clients import client_router
from routes.job import job_router

app = FastAPI()

# Include routers
app.include_router(serviceProvider, tags=["Service Providers"])
app.include_router(client_router, tags=["Clients"])
app.include_router(job_router, tags=["Jobs"])

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

