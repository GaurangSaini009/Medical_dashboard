from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('patients/', views.patients_view, name='patients'),
    path('add-patient/', views.add_patient_view, name='add_patient'),
    path('edit-patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete-patient/<int:id>/', views.delete_patient_view, name='delete_patient'),
    path('doctors/', views.doctors_view, name='doctors'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('add-appointment/', views.add_appointment, name='add_appointment'),
]