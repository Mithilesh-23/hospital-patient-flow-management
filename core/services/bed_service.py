from django.db import transaction

from core.models import Bed


VALID_TRANSITIONS = {
    Bed.Status.AVAILABLE: {
        Bed.Status.RESERVED,
        Bed.Status.MAINTENANCE,
        Bed.Status.OUT_OF_SERVICE,
    },
    Bed.Status.RESERVED: {
        Bed.Status.OCCUPIED,
        Bed.Status.AVAILABLE,
    },
    Bed.Status.OCCUPIED: {
        Bed.Status.CLEANING,
    },
    Bed.Status.CLEANING: {
        Bed.Status.AVAILABLE,
        Bed.Status.MAINTENANCE,
    },
    Bed.Status.MAINTENANCE: {
        Bed.Status.AVAILABLE,
        Bed.Status.OUT_OF_SERVICE,
    },
    Bed.Status.OUT_OF_SERVICE: {
        Bed.Status.AVAILABLE,
    },
}


def get_available_beds(hospital, bed_type=None, department=None):
    """Return beds currently available for assignment."""

    beds = Bed.objects.filter(
        hospital=hospital,
        status=Bed.Status.AVAILABLE,
        is_active=True,
    )

    if bed_type:
        beds = beds.filter(bed_type=bed_type)

    if department:
        beds = beds.filter(department=department)

    return beds


@transaction.atomic
def change_bed_status(bed, new_status):
    """Change bed status only when the transition is valid."""

    allowed_statuses = VALID_TRANSITIONS.get(bed.status, set())

    if new_status not in allowed_statuses:
        raise ValueError(
            f"Invalid bed transition: "
            f"{bed.status} -> {new_status}"
        )

    bed.status = new_status
    bed.save(update_fields=["status", "updated_at"])

    return bed