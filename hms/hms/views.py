from django.shortcuts import render,redirect
from .forms import DoctorForm,PatientForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from hmsApp.models import *
from google_auth_oauthlib.flow import Flow
import os,json
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import Group
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
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
    if request.method == "POST":

        form = DoctorForm(request.POST)

        if form.is_valid():

            user = form.save()

            Doctor.objects.create(
                user=user,
                specialization=form.cleaned_data["specialization"],
                phone=form.cleaned_data["phone"]
            )
            doctor_group, created = Group.objects.get_or_create(name='Doctor')
            user.groups.add(doctor_group)
            return redirect("login")

    form= DoctorForm()
    context = {
        'form':form,
    }
    return render(request,'signup.html',context)

def patient_signup(request):
    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():

            user = form.save()

            Patient.objects.create(
                user=user,
                phone=form.cleaned_data["phone"],
                date_of_birth=form.cleaned_data["date_of_birth"]
            )
            patient_group, created = Group.objects.get_or_create(name='Patient')
            user.groups.add(patient_group)
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

def logout_view(request):
    auth.logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    print('hiii')
    if hasattr(request.user, 'doctor'):
        return redirect('doc_slot')
    elif hasattr(request.user,'patient'):
        return redirect('view_doc')


# GOOGLE CALENDAR AUTHENTICATION

CLIENT_SECRETS_FILE = os.path.join(settings.BASE_DIR, 'oauth.json')
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
def google_auth_init(request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://127.0.0.1:8000/oauth2callback/'
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    request.session['oauth_state'] = state
    request.session['code_verifier'] = flow.code_verifier
    return redirect(authorization_url)

def google_auth_callback(request):
    state = request.session.get('oauth_state')
    code_verifier = request.session.get('code_verifier')
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri='http://127.0.0.1:8000/oauth2callback/'
    )
    flow.code_verifier = code_verifier
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    GoogleCredential.objects.update_or_create(
        user=request.user,
        defaults={
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': json.dumps(credentials.scopes),
        }
    )
    return redirect('dashboard')

