from django.db import transaction

from core.models import EmergencyCase


PRIORITY_ORDER = {
    EmergencyCase.Priority.P1: 1,
    EmergencyCase.Priority.P2: 2,
    EmergencyCase.Priority.P3: 3,
}


@transaction.atomic
def register_emergency(hospital, emergency_id, patient=None, notes=""):
    """Register a new emergency case."""

    return EmergencyCase.objects.create(
        hospital=hospital,
        patient=patient,
        emergency_id=emergency_id,
        notes=notes,
        status=EmergencyCase.Status.REGISTERED,
    )


@transaction.atomic
def triage_emergency(emergency_case, priority):
    """Assign emergency priority after medical staff triage."""

    if priority not in PRIORITY_ORDER:
        raise ValueError("Invalid emergency priority.")

    emergency_case.priority = priority
    emergency_case.status = EmergencyCase.Status.WAITING

    emergency_case.save(
        update_fields=["priority", "status"]
    )

    return emergency_case


def get_next_emergency(hospital):
    """
    Return the highest-priority waiting emergency.

    Priority:
    P1 → P2 → P3

    Same priority:
    Earlier arrival → served first
    """

    waiting_cases = (
        EmergencyCase.objects
        .filter(
            hospital=hospital,
            status=EmergencyCase.Status.WAITING,
            priority__isnull=False,
        )
        .order_by("arrival_time")
    )

    return min(
        waiting_cases,
        key=lambda case: PRIORITY_ORDER[case.priority],
        default=None,
    )


@transaction.atomic
def start_emergency_treatment(emergency_case):
    """Move an emergency case into treatment."""

    if emergency_case.status != EmergencyCase.Status.WAITING:
        raise ValueError("Emergency case is not waiting.")

    emergency_case.status = EmergencyCase.Status.IN_TREATMENT

    emergency_case.save(
        update_fields=["status"]
    )

    return emergency_case


@transaction.atomic
def complete_emergency(emergency_case):
    """Complete an emergency case."""

    if emergency_case.status != EmergencyCase.Status.IN_TREATMENT:
        raise ValueError("Emergency case is not currently in treatment.")

    emergency_case.status = EmergencyCase.Status.COMPLETED

    emergency_case.save(
        update_fields=["status"]
    )

    return emergency_case