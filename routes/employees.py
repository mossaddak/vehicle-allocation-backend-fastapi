from bson import ObjectId

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from config.database import connection

from helpers.employees import get_employee_data

from models.employees import Employee

employee_api = APIRouter()


@employee_api.post("/employees")
def create_employees(employee: Employee):
    connection.VEHICLE_ALLOCATION.employees.insert_one(dict(employee)).inserted_id
    return JSONResponse(
        content={"message": "Employee has been created."},
        status_code=status.HTTP_201_CREATED,
    )


@employee_api.get("/employees")
def get_employees():
    employees = [
        get_employee_data(employee)
        for employee in connection.VEHICLE_ALLOCATION.employees.find({})
    ]
    return JSONResponse(content=employees, status_code=status.HTTP_200_OK)


@employee_api.get("/employees/{id}")
def get_employee_details(id: str):

    employee = get_employee_data(
        connection.VEHICLE_ALLOCATION.employees.find_one({"_id": ObjectId(id)})
    )

    return JSONResponse(content=employee, status_code=status.HTTP_200_OK)
