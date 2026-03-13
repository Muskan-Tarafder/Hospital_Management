from django.shortcuts import render,redirect
from .forms import DoctorForm,PatientForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'doctor':
            return redirect('doctor_signup')
        elif role == 'patient':
            return redirect('patient_signup')
    return render(request, 'select_role.html')
    pass

def doctor_signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        form = DoctorForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=username,
                password=password
            )

            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()

            return redirect("login")
    form= DoctorForm()
    context = {
        'form':form,
    }
    return render(request,'signup.html',context)

def patient_signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        
        form = PatientForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=username,
                password=password
            )

            patient = form.save(commit=False)
            patient.user = user
            patient.save()

            return redirect("login")
    form= PatientForm()
    context = {
        'form':form,
    }
    return render(request,'signup.html',context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Log the user in
            from django.contrib.auth import login
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request,'login.html',context)

@login_required
def dashboard(request):
    print('hiii')
    if hasattr(request.user, 'doctor'):
        return redirect('doc_slot')
    elif hasattr(request.user,'patient'):
        return redirect('view_doc')

