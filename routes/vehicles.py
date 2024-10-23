from bson import ObjectId

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from config.database import connection

from helpers.employees import get_employee_data
from helpers.vehicles import get_vehicle_data

from models.vehicles import Vehicle

vehicle_api = APIRouter()


@vehicle_api.post("/vehicles")
def create_vehicles(vehicle: Vehicle):
    employee = connection.VEHICLE_ALLOCATION.employees.find_one(
        {"_id": ObjectId(vehicle.driver_id)}
    )
    if not employee or employee["role"] != "DRIVER":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No driver found!"
        )

    _vehicle = dict(vehicle)
    _vehicle.pop("driver_id")
    _vehicle["driver"] = dict(employee)
    connection.VEHICLE_ALLOCATION.vehicle.insert_one(_vehicle)
    return JSONResponse(
        content={"message": "Vehicle has been created."},
        status_code=status.HTTP_201_CREATED,
    )


@vehicle_api.get("/vehicles")
def get_vehicles():

    vehicles = [
        get_vehicle_data(vehicle)
        for vehicle in connection.VEHICLE_ALLOCATION.vehicle.find({})
    ]
    return JSONResponse(content=vehicles, status_code=status.HTTP_200_OK)


@vehicle_api.get("/vehicles/{id}")
def get_vehicle_details(id: str):
    vehicle = connection.VEHICLE_ALLOCATION.vehicle.find_one({"_id": ObjectId(id)})

    _vehicle = {
        **get_vehicle_data(vehicle),
        "employee": get_employee_data(
            connection.VEHICLE_ALLOCATION.employees.find_one(
                {"_id": ObjectId(vehicle["driver"]["_id"])}
            )
        ),
    }
    return JSONResponse(content=_vehicle, status_code=status.HTTP_200_OK)
