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