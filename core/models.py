from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        RECEPTIONIST = "RECEPTIONIST", "Receptionist"
        DOCTOR = "DOCTOR", "Doctor"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT,
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="departments",
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hospital.name} - {self.name}"


class Doctor(models.Model):

    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        BUSY = "BUSY", "Busy"
        BREAK = "BREAK", "Break"
        OFFLINE = "OFFLINE", "Offline"
        EMERGENCY = "EMERGENCY", "Emergency"
        LEAVE = "LEAVE", "Leave"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="doctors",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="doctors",
    )
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    availability_status = models.CharField(
        max_length=20,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.OFFLINE,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"


class Staff(models.Model):

    class StaffType(models.TextChoices):
        RECEPTIONIST = "RECEPTIONIST", "Receptionist"
        NURSE = "NURSE", "Nurse"
        BED_MANAGER = "BED_MANAGER", "Bed Manager"
        TRIAGE = "TRIAGE", "Triage Staff"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="staff",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff",
    )
    staff_type = models.CharField(
        max_length=20,
        choices=StaffType.choices,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.staff_type}"

class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    patient_id = models.CharField(
        max_length=20,
        unique=True,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=20,
        blank=True,
    )
    blood_group = models.CharField(
        max_length=5,
        blank=True,
    )
    address = models.TextField(
        blank=True,
    )
    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
    )
    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.patient_id} - {self.user.get_full_name()}"


class Appointment(models.Model):

    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        CHECKED_IN = "CHECKED_IN", "Checked In"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        NO_SHOW = "NO_SHOW", "No Show"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
    )

    reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.patient.patient_id} - "
            f"{self.appointment_date} {self.appointment_time}"
        )


class Queue(models.Model):
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="queues",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="queues",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="queues",
    )
    date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.department.name} - {self.date}"



class QueueEntry(models.Model):

    class Status(models.TextChoices):
        WAITING = "WAITING", "Waiting"
        CALLED = "CALLED", "Called"
        IN_CONSULTATION = "IN_CONSULTATION", "In Consultation"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        NO_SHOW = "NO_SHOW", "No Show"

    queue = models.ForeignKey(
        Queue,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="queue_entries",
    )
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="queue_entry",
    )

    token_number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WAITING,
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    called_at = models.DateTimeField(null=True, blank=True)
    consultation_started_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Token {self.token_number} - {self.patient.patient_id}"


class EmergencyCase(models.Model):

    class Priority(models.TextChoices):
        P1 = "P1", "Critical"
        P2 = "P2", "Urgent"
        P3 = "P3", "Lower Urgency"

    class Status(models.TextChoices):
        REGISTERED = "REGISTERED", "Registered"
        TRIAGED = "TRIAGED", "Triaged"
        WAITING = "WAITING", "Waiting"
        IN_TREATMENT = "IN_TREATMENT", "In Treatment"
        COMPLETED = "COMPLETED", "Completed"
        TRANSFERRED = "TRANSFERRED", "Transferred"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_cases",
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="emergency_cases",
    )

    emergency_id = models.CharField(
        max_length=30,
        unique=True,
    )

    priority = models.CharField(
        max_length=2,
        choices=Priority.choices,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REGISTERED,
    )

    arrival_time = models.DateTimeField(
        auto_now_add=True,
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.emergency_id

class EmergencyCase(models.Model):
    class Priority(models.TextChoices):
        P1 = "P1", "Critical"
        P2 = "P2", "Urgent"
        P3 = "P3", "Lower Urgency"

    class Status(models.TextChoices):
        REGISTERED = "REGISTERED", "Registered"
        TRIAGED = "TRIAGED", "Triaged"
        WAITING = "WAITING", "Waiting"
        IN_TREATMENT = "IN_TREATMENT", "In Treatment"
        COMPLETED = "COMPLETED", "Completed"
        TRANSFERRED = "TRANSFERRED", "Transferred"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_cases",
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="emergency_cases",
    )

    emergency_id = models.CharField(
        max_length=30,
        unique=True
    )

    priority = models.CharField(
        max_length=2,
        choices=Priority.choices,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REGISTERED,
    )

    arrival_time = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.emergency_id


class Bed(models.Model):
    class BedType(models.TextChoices):
        GENERAL = "GENERAL", "General"
        SEMI_PRIVATE = "SEMI_PRIVATE", "Semi Private"
        PRIVATE = "PRIVATE", "Private"
        ICU = "ICU", "ICU"
        EMERGENCY = "EMERGENCY", "Emergency"

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        RESERVED = "RESERVED", "Reserved"
        OCCUPIED = "OCCUPIED", "Occupied"
        CLEANING = "CLEANING", "Cleaning"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        OUT_OF_SERVICE = "OUT_OF_SERVICE", "Out of Service"

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="beds",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="beds",
    )

    bed_number = models.CharField(max_length=20)

    bed_type = models.CharField(
        max_length=20,
        choices=BedType.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    floor = models.CharField(max_length=20, blank=True)

    room_number = models.CharField(max_length=20, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hospital.name} - Bed {self.bed_number}"