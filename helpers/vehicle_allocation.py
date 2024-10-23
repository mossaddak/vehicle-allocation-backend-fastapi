def get_vechicle_allocation_data(vehicle_allocation):
    return {
        "id": str(vehicle_allocation["_id"]),
        "allocation_date": vehicle_allocation["allocation_date"],
    }
