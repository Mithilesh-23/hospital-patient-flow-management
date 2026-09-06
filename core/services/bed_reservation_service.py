from django.db import transaction
from core.models import Bed, BedReservation


@transaction.atomic
def reserve_bed(bed, patient, expected_arrival=None, expires_at=None, notes=""):
    """
    Reserve an available bed for a patient.
    """

    if bed.status != Bed.Status.AVAILABLE:
        raise ValueError(
            f"Bed {bed.bed_number} is not available for reservation."
        )

    bed.status = Bed.Status.RESERVED
    bed.save(update_fields=["status", "updated_at"])

    reservation = BedReservation.objects.create(
        bed=bed,
        patient=patient,
        expected_arrival=expected_arrival,
        expires_at=expires_at,
        notes=notes,
        status=BedReservation.Status.ACTIVE,
    )

    return reservation


@transaction.atomic
def confirm_reservation(reservation):
    """
    Confirm an active bed reservation.
    """

    if reservation.status != BedReservation.Status.ACTIVE:
        raise ValueError(
            f"Cannot confirm reservation with status: {reservation.status}"
        )

    reservation.status = BedReservation.Status.CONFIRMED
    reservation.save(update_fields=["status"])

    return reservation


@transaction.atomic
def cancel_reservation(reservation):
    """
    Cancel a reservation and make the bed available again.
    """

    if reservation.status not in [
        BedReservation.Status.ACTIVE,
        BedReservation.Status.CONFIRMED,
    ]:
        raise ValueError(
            f"Cannot cancel reservation with status: {reservation.status}"
        )

    bed = reservation.bed

    reservation.status = BedReservation.Status.CANCELLED
    reservation.save(update_fields=["status"])

    if bed.status == Bed.Status.RESERVED:
        bed.status = Bed.Status.AVAILABLE
        bed.save(update_fields=["status", "updated_at"])

    return reservation