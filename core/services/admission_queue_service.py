from django.db import transaction
from core.models import AdmissionQueueEntry


PRIORITY_ORDER = {
    AdmissionQueueEntry.Priority.CRITICAL: 1,
    AdmissionQueueEntry.Priority.URGENT: 2,
    AdmissionQueueEntry.Priority.NORMAL: 3,
}


@transaction.atomic
def add_to_admission_queue(
    patient,
    hospital,
    department,
    requested_bed_type,
    priority=AdmissionQueueEntry.Priority.NORMAL,
    notes="",
):
    """
    Add a patient to the admission queue.
    """

    if priority not in PRIORITY_ORDER:
        raise ValueError(f"Invalid admission priority: {priority}")

    if not requested_bed_type:
        raise ValueError("Requested bed type is required.")

    entry = AdmissionQueueEntry.objects.create(
        patient=patient,
        hospital=hospital,
        department=department,
        requested_bed_type=requested_bed_type,
        priority=priority,
        status=AdmissionQueueEntry.Status.WAITING,
        notes=notes,
    )

    return entry


def get_next_admission(hospital, bed_type=None):
    """
    Return the highest-priority waiting admission.

    Priority:
    CRITICAL → URGENT → NORMAL

    Same priority:
    Earlier request time first.
    """

    entries = AdmissionQueueEntry.objects.filter(
        hospital=hospital,
        status=AdmissionQueueEntry.Status.WAITING,
    ).order_by("requested_at")

    if bed_type:
        entries = entries.filter(requested_bed_type=bed_type)

    return min(
        entries,
        key=lambda entry: PRIORITY_ORDER[entry.priority],
        default=None,
    )


@transaction.atomic
def cancel_admission_request(entry):
    """
    Cancel a waiting admission request.
    """

    if entry.status != AdmissionQueueEntry.Status.WAITING:
        raise ValueError(
            f"Cannot cancel admission with status: {entry.status}"
        )

    entry.status = AdmissionQueueEntry.Status.CANCELLED
    entry.save(update_fields=["status"])

    return entry