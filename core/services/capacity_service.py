from core.models import Bed


def get_hospital_capacity(hospital):
    beds = Bed.objects.filter(hospital=hospital)

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
        "total": total,
        "available": available,
        "reserved": reserved,
        "occupied": occupied,
        "cleaning": cleaning,
        "maintenance": maintenance,
        "occupancy_percentage": round(occupancy_percentage, 2),
    }