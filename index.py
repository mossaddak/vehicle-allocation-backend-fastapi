from fastapi import FastAPI
from routes.vehicles import vehicle_api
from routes.employees import employee_api
from routes.vehicle_allocation import vehicle_allocation_api

app = FastAPI()

# Routes
app.include_router(vehicle_api, prefix="/api/v1")
app.include_router(employee_api, prefix="/api/v1")
app.include_router(vehicle_allocation_api, prefix="/api/v1")
