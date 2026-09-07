from core.models import Bed


def get_department_capacity(department):
    beds = Bed.objects.filter(department=department)

    total = beds.count()
    available = beds.filter(status=Bed.Status.AVAILABLE).count()
    reserved = beds.filter(status=Bed.Status.RESERVED).count()
    occupied = beds.filter(status=Bed.Status.OCCUPIED).count()
    cleaning = beds.filter(status=Bed.Status.CLEANING).count()
    maintenance = beds.filter(status=Bed.Status.MAINTENANCE).count()

    occupancy_percentage = (
        (occupied / total) * 100
        if total > 0
        else 0
    )

    return {
        "department": department.name,
        "total": total,
        "available": available,
        "reserved": reserved,
        "occupied": occupied,
        "cleaning": cleaning,
        "maintenance": maintenance,
        "occupancy_percentage": round(occupancy_percentage, 2),
    }