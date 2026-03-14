from django import forms
from hmsApp.models import Doctor,Patient
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm



class DoctorForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email =  forms.EmailField(max_length=40)
    specialization = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2"
        ]


class PatientForm(UserCreationForm):

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email =  forms.EmailField(max_length=40)
    phone = forms.CharField(max_length=15)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type':'date'})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2"
        ]


