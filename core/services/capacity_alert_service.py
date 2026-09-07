from core.services.capacity_service import get_hospital_capacity


def get_capacity_alert(hospital):
    capacity = get_hospital_capacity(hospital)
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
        "level": level,
        "occupancy_percentage": occupancy,
        "message": f"Hospital occupancy is {occupancy}%. Status: {level}.",
    }