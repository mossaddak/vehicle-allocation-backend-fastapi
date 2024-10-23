from pydantic import BaseModel

from .choices import EmployeeRole


class Employee(BaseModel):
    name: str
    role: EmployeeRole
