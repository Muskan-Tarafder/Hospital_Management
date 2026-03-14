from django.contrib.auth.models import Group

from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import AvailabilityForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def create_calendar_event(user, slot):
    try:
        creds_data = GoogleCredential.objects.get(user=user)
        credentials = Credentials(
            token=creds_data.token,
            refresh_token=creds_data.refresh_token,
            token_uri=creds_data.token_uri,
            client_id=creds_data.client_id,
            client_secret=creds_data.client_secret
        )

        service = build('calendar', 'v3', credentials=credentials)
        
        start_dt = f"{slot.date}T{slot.start_time}"
        end_dt = f"{slot.date}T{slot.end_time}"

        event = {
            'summary': f'Medical Appointment: {slot.doctor.user.get_full_name()}',
            'description': 'Appointment booked via CareSync HMS',
            'start': {
                'dateTime': start_dt,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_dt,
                'timeZone': 'Asia/Kolkata',
            },
        }
        
        print(f"Attempting to create event: {event}")
        service.events().insert(calendarId='primary', body=event).execute()
        print('Event added')
    except Exception as e:
        print(f"Error creating calendar event: {e}")


def trigger_email_notification(recipient_email, patient_name, doctor_name, date, time):
    payload = {
        "email": recipient_email,
        "subject": "Appointment Confirmation - CareSync",
        "message": f"Hello {patient_name},\n\nYour appointment with Dr. {doctor_name} is confirmed for {date} at {time}.\n\nThank you for using CareSync!"
    }
    try:
        # Serverless Offline endpoint
        requests.post("http://localhost:3000/dev/send-email", json=payload)
    except Exception as e:
        print(f"Email service error: {e}")

# PATIENT: View doctors
@login_required(login_url='login')
def view_doc(request):

    if not request.user.groups.filter(name="Patient").exists():
        return redirect("dashboard")

    doctors = Doctor.objects.all()
    context = {
        'doctors':doctors,
    }
    print(doctors)
    return render(request,'dashboard.html',context)


@login_required(login_url='login')
def view_slot(request, doctor_id):

    if not request.user.groups.filter(name="Patient").exists():
        return redirect("dashboard")

    doctor = get_object_or_404(Doctor, id=doctor_id)

    slots = AvailabilitySlot.objects.filter(
        doctor=doctor,
        is_booked=False
    ).order_by('date','start_time')

    context = {
        'slots': slots,
        'doctor': doctor
    }

    return render(request, 'view_slot.html', context)


# DOCTOR: create slot
@login_required(login_url='login')
def create_slot(request):

    if not request.user.groups.filter(name="Doctor").exists():
        return redirect("dashboard")

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


@login_required(login_url='login')
def doc_slot(request):

    if not request.user.groups.filter(name="Doctor").exists():
        return redirect("dashboard")

    doctor = request.user.doctor
    slots = AvailabilitySlot.objects.filter(doctor=doctor)

    context = {
        'slots':slots,
    }

    return render(request,'dashboard.html',context)


@login_required(login_url='login')
def update_slot(request,slot_id):

    if not request.user.groups.filter(name="Doctor").exists():
        return redirect("dashboard")

    slot = AvailabilitySlot.objects.get(id=slot_id)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST,instance=slot)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    form = AvailabilityForm(instance=slot)

    context = {
        'form':form,
    }

    return render(request,'create_slot.html',context)


@login_required(login_url='login')
def cancel_booking(request,slot_id):

    if not request.user.groups.filter(name="Doctor").exists():
        return redirect("dashboard")

    booking = get_object_or_404(Booking, slot_id=slot_id)

    slot = booking.slot
    slot.is_booked = False
    slot.save()

    booking.delete()

    return redirect('dashboard')


# PATIENT: book slot
@login_required(login_url='login')
def book_slot(request,slot_id):

    if not request.user.groups.filter(name="Patient").exists():
        return redirect("dashboard")

    slot = get_object_or_404(AvailabilitySlot, id=slot_id)

    if slot.is_booked:
        return redirect('view_doc')

    Booking.objects.create(
        patient=request.user.patient,
        slot=slot
    )

    slot.is_booked = True
    slot.save()

    # Trigger Calendar for Patient
    create_calendar_event(request.user, slot)
    # Trigger Calendar for Doctor
    create_calendar_event(slot.doctor.user, slot)

    trigger_email_notification(
        recipient_email='muskantarafder1520@gmail.com', #request.user.email
        patient_name=request.user.get_full_name() or request.user.username,
        doctor_name=slot.doctor.user.get_full_name() or slot.doctor.user.username,
        date=str(slot.date),
        time=str(slot.start_time)
    )
    return redirect('view_doc')


@login_required(login_url='login')
def view_booking(request,patient_id):

    if not request.user.groups.filter(name="Patient").exists():
        return redirect("dashboard")
    if request.user.patient.id != patient_id:
        raise PermissionDenied
    appointment = Booking.objects.filter(patient=request.user.patient)
    context = {
        'bookings':appointment,
    }

    return render(request,'my_bookings.html',context)


# from django.shortcuts import render,redirect,get_object_or_404
# from .models import *
# from .forms import AvailabilityForm
# from django.contrib.auth.decorators import login_required
# # Create your views here.

# @login_required(login_url='login')
# def view_doc(request):
#     doctors = Doctor.objects.all()
#     context = {
#         'doctors':doctors,
#     }
#     print(doctors)
#     return render(request,'dashboard.html',context)


# def view_slot(request, doctor_id):

#     doctor = get_object_or_404(Doctor, id=doctor_id)

#     slots = AvailabilitySlot.objects.filter(
#         doctor=doctor,
#         is_booked=False
#     ).order_by('date','start_time')

#     context = {
#         'slots': slots,
#         'doctor': doctor
#     }

#     return render(request, 'view_slot.html', context)
# def create_slot(request):
#     if not hasattr(request.user, "doctor"):
#         return redirect("dashboard")
#     if request.method == 'POST':
#         form = AvailabilityForm(request.POST)
#         if form.is_valid():
#             slot = form.save(commit=False)
#             slot.doctor = request.user.doctor
#             slot.save()
#             return redirect('dashboard')
#     form = AvailabilityForm()
#     context = {
#         'form':form,
#     }
#     return render(request,'create_slot.html',context)

# def doc_slot(request):
#     doctor =  request.user.doctor
#     slots = AvailabilitySlot.objects.filter(doctor=doctor)
#     context = {
#         'slots':slots,
#     }
#     return render(request,'dashboard.html',context)

# def update_slot(request,slot_id):
#     if not hasattr(request.user, "doctor"):
#         return redirect("dashboard")
#     slot = AvailabilitySlot.objects.get(id=slot_id)
#     if request.method == 'POST':
#         form = AvailabilityForm(request.POST,instance=slot)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     form = AvailabilityForm(instance=slot)
#     context = {
#         'form':form,
#     }
#     return render(request,'create_slot.html',context)

# def cancel_booking(request,slot_id):
#     if not hasattr(request.user, "doctor"):
#         return redirect("dashboard")
#     booking =  get_object_or_404(Booking, slot_id=slot_id)
#     slot =  booking.slot
#     slot.is_booked = False
#     slot.save()
#     booking.delete()
#     return redirect('dashboard')

# def book_slot(request,slot_id):
#     slot = get_object_or_404(AvailabilitySlot, id=slot_id)
#     if slot.is_booked:
#         return redirect('view_doc')
    
#     Booking.objects.create(
#         patient=request.user.patient,
#         slot=slot
#     )
#     slot.is_booked = True
#     slot.save()
#     return redirect('view_doc')

# def view_booking(request,patient_id):
#     appointment = Booking.objects.filter(patient_id=patient_id)
#     context = {
#         'bookings':appointment,
#     }
#     return render(request,'my_bookings.html',context)