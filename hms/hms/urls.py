"""
URL configuration for hms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from hmsApp import views as hms_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signup/doctor/',views.doctor_signup,name='doctor_signup'),
    path('signup/patient/',views.patient_signup,name='patient_signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),

    path('dashboard/',views.dashboard,name='dashboard'),
    path('view_doc/',hms_view.view_doc,name='view_doc'),
    path('view_slot/<int:doctor_id>',hms_view.view_slot,name='view_slot'),
    path('book_slot/<int:slot_id>/',hms_view.book_slot,name='book_slot'),
    path('view_booking/<int:patient_id>',hms_view.view_booking,name='view_booking'),

    path('create_slot/',hms_view.create_slot,name='create_slot'),
    path('doc_slot/',hms_view.doc_slot,name='doc_slot'),
    path('update_slot/<int:slot_id>/',hms_view.update_slot,name='update_slot'),
    path('cancel_booking/<int:slot_id>/',hms_view.cancel_booking,name='cancel_booking'),

    path('connect_google/',views.google_auth_init,name='connect_google'),
    path('oauth2callback/', views.google_auth_callback, name='oauthcallback')
]

