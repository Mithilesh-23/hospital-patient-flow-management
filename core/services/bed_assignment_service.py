from django.db import transaction
from core.models import Bed, BedReservation


@transaction.atomic
def assign_reserved_bed(reservation):
    """
    Safely assign a reserved bed to the patient.

    select_for_update() locks the bed row during the transaction,
    preventing another transaction from assigning the same bed.
    """

    locked_bed = Bed.objects.select_for_update().get(
        id=reservation.bed_id
    )

    if reservation.status not in [
        BedReservation.Status.ACTIVE,
        BedReservation.Status.CONFIRMED,
    ]:
        raise ValueError(
            f"Cannot assign bed for reservation status: "
            f"{reservation.status}"
        )

    if locked_bed.status != Bed.Status.RESERVED:
        raise ValueError(
            f"Bed {locked_bed.bed_number} is not reserved."
        )

    locked_bed.status = Bed.Status.OCCUPIED
    locked_bed.save(update_fields=["status", "updated_at"])

    reservation.status = BedReservation.Status.CONVERTED_TO_OCCUPIED
    reservation.save(update_fields=["status"])

    return locked_bed