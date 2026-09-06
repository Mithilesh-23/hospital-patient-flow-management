from django.db import transaction
from django.utils import timezone

from core.models import Queue, QueueEntry


@transaction.atomic
def generate_token(queue, patient, appointment=None):
    """Create a queue entry and generate the next token."""

    last_entry = (
        QueueEntry.objects
        .filter(queue=queue)
        .order_by("-token_number")
        .first()
    )

    next_token = 1 if last_entry is None else last_entry.token_number + 1

    return QueueEntry.objects.create(
        queue=queue,
        patient=patient,
        appointment=appointment,
        token_number=next_token,
        status=QueueEntry.Status.WAITING,
    )


def get_next_patient(queue):
    """Return the first waiting patient using FIFO."""

    return (
        QueueEntry.objects
        .filter(
            queue=queue,
            status=QueueEntry.Status.WAITING,
        )
        .order_by("joined_at", "token_number")
        .first()
    )


@transaction.atomic
def call_next_patient(queue):
    """Call the next patient in the FIFO queue."""

    entry = get_next_patient(queue)

    if entry is None:
        return None

    entry.status = QueueEntry.Status.CALLED
    entry.called_at = timezone.now()

    entry.save(
        update_fields=["status", "called_at"]
    )

    return entry