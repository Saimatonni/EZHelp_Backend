from fastapi import FastAPI
from routes.serviceProviders import serviceProvider
from routes.clients import client_router
from routes.job import job_router
app = FastAPI()
# app.include_router(serviceProvider)
# app.include_router(client_router)
# app.include_router(job_router)
app.include_router(serviceProvider, tags=["Service Providers"])
app.include_router(client_router, tags=["Clients"])
app.include_router(job_router, tags=["Jobs"])
