def get_vehicle_data(vehicle):
    return {
        "id": str(vehicle["_id"]),
        "title": vehicle["title"],
        "kind":vehicle["kind"]
    }
