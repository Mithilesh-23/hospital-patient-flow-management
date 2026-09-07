from core.models import QueueEntry


def predict_wait_time(queue_entry):
    """
    Estimate waiting time using the average duration
    of the last 5 completed consultations.
    """

    completed_entries = QueueEntry.objects.filter(
        queue=queue_entry.queue,
        status=QueueEntry.Status.COMPLETED,
        consultation_started_at__isnull=False,
        completed_at__isnull=False,
    ).order_by("-completed_at")[:5]

    durations = []

    for entry in completed_entries:
        duration = (
            entry.completed_at - entry.consultation_started_at
        ).total_seconds() / 60

        durations.append(duration)

    if durations:
        average_time = sum(durations) / len(durations)
    else:
        average_time = 15

    patients_ahead = QueueEntry.objects.filter(
        queue=queue_entry.queue,
        status=QueueEntry.Status.WAITING,
        token_number__lt=queue_entry.token_number,
    ).count()

    estimated_wait = average_time * patients_ahead

    return {
        "patients_ahead": patients_ahead,
        "average_consultation_time": round(average_time, 2),
        "estimated_wait_minutes": round(estimated_wait, 2),
    }