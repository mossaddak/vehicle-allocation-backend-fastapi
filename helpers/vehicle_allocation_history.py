from bson import ObjectId

from fastapi import HTTPException, status

from config.database import connection


def create_allocation_history(allocation_id, kind):
    allocation = connection.VEHICLE_ALLOCATION.vehicle_allocation.find_one(
        {"_id": ObjectId(allocation_id)}
    )
    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No driver found!"
        )

    history = {"allocation": allocation_id, "kind": kind}
    return connection.VEHICLE_ALLOCATION.vehicle_allocation_history.insert_one(history)
