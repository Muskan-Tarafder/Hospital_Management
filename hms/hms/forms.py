from django import forms
from hmsApp.models import Doctor,Patient
from django.contrib.auth.models import User
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'phone']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
