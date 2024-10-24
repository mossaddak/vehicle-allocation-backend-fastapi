from bson import ObjectId

from datetime import datetime

from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse

from config.database import connection

from helpers.employees import get_employee_data
from helpers.vehicles import get_vehicle_data
from helpers.vehicle_allocation import get_vechicle_allocation_data
from helpers.vehicle_allocation_history import create_allocation_history

from models.choices import VehicleAllocationHistory
from models.vehicle_allocation import VehicleAllocation

vehicle_allocation_api = APIRouter()


@vehicle_allocation_api.post("/vehicle-allocations")
def create_vehicle_allocation(vehicle_allocation: VehicleAllocation):

    # get employee
    employee = connection.VEHICLE_ALLOCATION.employees.find_one(
        {"_id": ObjectId(vehicle_allocation.employee_id)}
    )
    if employee["role"] == "DRIVER":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No driver found!"
        )

    # Checking the vehicle available or not on the same date
    employee_allocation = connection.VEHICLE_ALLOCATION.vehicle_allocation.find_one(
        {
            "vehicle._id": ObjectId(vehicle_allocation.vehicle_id),
            "allocation_date": vehicle_allocation.allocation_date,
        }
    )
    if employee_allocation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This vechicle is already assigned on this date!",
        )

    # get vechile
    vehicle = connection.VEHICLE_ALLOCATION.vehicle.find_one(
        {"_id": ObjectId(vehicle_allocation.vehicle_id)}
    )

    _vehicle_allocation = dict(vehicle_allocation)  # converting into dictionary
    _vehicle_allocation["employee"] = employee
    _vehicle_allocation["vehicle"] = vehicle

    # Removing the related ids
    _vehicle_allocation.pop("employee_id")
    _vehicle_allocation.pop("vehicle_id")

    # Create vehicle allocation
    vehicle_allocation = connection.VEHICLE_ALLOCATION.vehicle_allocation.insert_one(
        _vehicle_allocation
    )

    # Crete history
    create_allocation_history(
        str(vehicle_allocation.inserted_id), VehicleAllocationHistory.CREATED
    )
    return JSONResponse(
        content={"message": "Vehicle allocation has been created."},
        status_code=status.HTTP_201_CREATED,
    )


@vehicle_allocation_api.get("/vehicle-allocations")
def get_vehicle_allocations():
    vehicles = [
        get_vechicle_allocation_data(vehicle_allocation)
        for vehicle_allocation in connection.VEHICLE_ALLOCATION.vehicle_allocation.find(
            {}
        )
    ]
    return JSONResponse(content=vehicles, status_code=status.HTTP_200_OK)


@vehicle_allocation_api.get("/vehicle-allocations/{id}")
def get_vehicle_allocation_details(id: str):
    vehicle_allocation = connection.VEHICLE_ALLOCATION.vehicle_allocation.find_one(
        {"_id": ObjectId(id)}
    )
    if not vehicle_allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle allocation not found"
        )

    _vehicle_allocation = {
        **get_vechicle_allocation_data(vehicle_allocation),
        "employee": get_employee_data(
            connection.VEHICLE_ALLOCATION.employees.find_one(
                {"_id": ObjectId(vehicle_allocation["employee"]["id"])}
            )
        ),
        "vehicle": get_vehicle_data(
            connection.VEHICLE_ALLOCATION.vehicle.find_one(
                {"_id": ObjectId(vehicle_allocation["vehicle"]["id"])}
            )
        ),
    }
    return JSONResponse(content=_vehicle_allocation, status_code=status.HTTP_200_OK)


@vehicle_allocation_api.patch("/vehicle-allocations/{id}")
def update_vehicle_allocation(id: str, data: dict = Body(...)):

    update_data = {}
    vehicle_allocation = connection.VEHICLE_ALLOCATION.vehicle_allocation.find_one(
        {"_id": ObjectId(id)}
    )

    if not vehicle_allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle allocation not found!",
        )

    # Check if employee needs to be updated
    if "employee_id" in data:
        employee = connection.VEHICLE_ALLOCATION.employees.find_one(
            {"_id": ObjectId(data["employee_id"])}
        )
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Employee not found"
            )
        update_data["employee"] = get_employee_data(employee)

    # Check if vehicle needs to be updated
    if "vehicle_id" in data:
        vehicle = connection.VEHICLE_ALLOCATION.vehicle.find_one(
            {"_id": ObjectId(data["vehicle_id"])}
        )
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle not found"
            )
        update_data["vehicle"] = get_vehicle_data(vehicle)

    # Other fields like allocation_date can also be updated
    if "allocation_date" in data:
        today = datetime.today().date()
        # Convert the string allocation date to a datetime.date object
        current_allocation_date = datetime.strptime(
            vehicle_allocation["allocation_date"], "%Y-%m-%d"
        ).date()
        request_allocation_date = datetime.strptime(
            data["allocation_date"], "%Y-%m-%d"
        ).date()
        if current_allocation_date < today > request_allocation_date:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Time has been exceeded!"
            )
        update_data["allocation_date"] = data["allocation_date"]

    vehicle_allocation = connection.VEHICLE_ALLOCATION.vehicle_allocation.update_one(
        {"_id": ObjectId(id)}, {"$set": update_data}
    )
    # Crete history
    create_allocation_history(id, VehicleAllocationHistory.UPDATED)
    return JSONResponse(
        content={"message": "Vehicel alocation updated successfully."},
        status_code=status.HTTP_200_OK,
    )


@vehicle_allocation_api.delete("/vehicle-allocations/{id}")
def delete_vehicle_allocation(id: str):
    vehicle_allocation = connection.VEHICLE_ALLOCATION.vehicle_allocation.find_one(
        {"_id": ObjectId(id)}
    )

    if not vehicle_allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle allocation not found!",
        )

    today = datetime.today().date()
    allocation_date = datetime.strptime(
        vehicle_allocation["allocation_date"], "%Y-%m-%d"
    ).date()

    # Deleted before the allocation date
    if today < allocation_date:
        connection.VEHICLE_ALLOCATION.vehicle_allocation.delete_one(
            {"_id": ObjectId(id)}
        )

        return JSONResponse(
            content={"message": "Vehicel allocation has been deleted successfully."},
            status_code=status.HTTP_200_OK,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Time has been exceeded!"
        )
