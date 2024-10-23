from pydantic import BaseModel

from .choices import VehicleKind


class Vehicle(BaseModel):
    title: str
    kind: VehicleKind
    driver_id: str


