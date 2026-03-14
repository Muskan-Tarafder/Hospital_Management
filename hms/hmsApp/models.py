from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True,default='temp@gmail.com')

    def __str__(self):
        return f"Dr. {self.user.username}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True,default='temp@gmail.com')
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
        return f'{self.patient} booked {self.slot}'

class GoogleCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scopes = models.TextField()

    