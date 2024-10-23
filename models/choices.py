from enum import Enum
from pydantic import BaseModel


class EmployeeRole(str, Enum):
    DRIVER = "DRIVER"
    FRONTEND_ENGINEER = "FRONTEND_ENGINEER"
    BACKEND_ENGINEER = "BACKEND_ENGINEER"


class VehicleKind(str, Enum):
    PRIVATE_CAR = "PRIVATE_CAR"
    BUS = "BUS"
    VAN = "VAN"


class VehicleAllocationHistory(str, Enum):
    UPDATED = "UPDATED"
    CREATED = "CREATED"
