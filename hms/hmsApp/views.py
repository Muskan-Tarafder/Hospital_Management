from django.shortcuts import render,redirect
from .models import *
from .forms import AvailabilityForm
# Create your views here.


def view_doc(request):
    doctors = Doctor.objects.all()
    context = {
        'doctors':doctors,
    }
    print(doctors)
    return render(request,'dashboard.html',context)

def view_slot(request):

    return render(request,'view_slot.html')

def create_slot(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user.doctor
            slot.save()
            return redirect('dashboard')
    form = AvailabilityForm()
    context = {
        'form':form,
    }
    return render(request,'create_slot.html',context)
