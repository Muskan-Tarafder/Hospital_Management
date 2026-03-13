from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.user.username}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}"
    
class Booking(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    slot = models.OneToOneField(AvailabilitySlot,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{self.patient} booked {self.slot}'
    