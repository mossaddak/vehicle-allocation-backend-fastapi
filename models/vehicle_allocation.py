from pydantic import BaseModel

class VehicleAllocation(BaseModel):
    allocation_date: str
    employee_id: str
    vehicle_id: str

class VehicleAllocationSession(BaseModel):
    allocation_date: str
    kind: str
