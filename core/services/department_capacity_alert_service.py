from core.services.department_capacity_service import get_department_capacity


def get_department_capacity_alert(department):
    capacity = get_department_capacity(department)
    occupancy = capacity["occupancy_percentage"]

    if occupancy > 95:
        level = "CRITICAL"
    elif occupancy >= 85:
        level = "HIGH"
    elif occupancy >= 70:
        level = "MODERATE"
    else:
        level = "NORMAL"

    return {
        "department": department.name,
        "level": level,
        "occupancy_percentage": occupancy,
        "message": (
            f"{department.name} occupancy is "
            f"{occupancy}%. Status: {level}."
        ),
    }