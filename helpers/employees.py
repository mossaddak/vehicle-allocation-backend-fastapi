def get_employee_data(employee):
    return {
        "id": str(employee["_id"]),
        "name": employee["name"],
        "role": employee["role"],
    }
