from .models import *
from django import forms
class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = AvailabilitySlot
        fields = ['date', 'start_time', 'end_time']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class SlotFilterForm(forms.Form):

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        label="Select Doctor"
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Select Date"
    )