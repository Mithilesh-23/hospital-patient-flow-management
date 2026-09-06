from core.models import Doctor, QueueEntry


def get_available_doctors(department):
    """Return active doctors currently available in a department."""

    return Doctor.objects.filter(
        department=department,
        is_active=True,
        availability_status=Doctor.AvailabilityStatus.AVAILABLE,
    )


def get_doctor_workload(doctor):
    """Count patients currently waiting or being treated by a doctor."""

    return QueueEntry.objects.filter(
        queue__doctor=doctor,
        status__in=[
            QueueEntry.Status.WAITING,
            QueueEntry.Status.CALLED,
            QueueEntry.Status.IN_CONSULTATION,
        ],
    ).count()


def select_doctor(department):
    """
    Select an available doctor using a simple
    load-balancing strategy.

    Doctor with the lowest current workload is selected.
    """

    doctors = get_available_doctors(department)

    if not doctors.exists():
        return None

    return min(
        doctors,
        key=get_doctor_workload,
    )