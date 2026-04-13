from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Patient
from .forms import PatientForm


# ---------------- HOME / STATIC PAGES ----------------

def home_view(request):
    return render(request, 'accounts/home.html')


def about_view(request):
    return render(request, 'accounts/about.html')


def services_view(request):
    return render(request, 'accounts/services.html')


def contact_view(request):
    return render(request, 'accounts/contact.html')


# ---------------- AUTH ----------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


# ---------------- DASHBOARD ----------------

def dashboard_view(request):
    total_patients = Patient.objects.count()
    male_patients = Patient.objects.filter(gender='Male').count()
    female_patients = Patient.objects.filter(gender='Female').count()
    recent_patients = Patient.objects.filter(
        date_added__gte=timezone.now() - timedelta(days=7)
    ).count()

    context = {
        'total_patients': total_patients,
        'male_patients': male_patients,
        'female_patients': female_patients,
        'recent_patients': recent_patients,
    }
    return render(request, 'accounts/dashboard.html', context)


# ---------------- PATIENT CRUD ----------------

def patients_view(request):
    patients = Patient.objects.all().order_by('-date_added')
    return render(request, 'accounts/patients.html', {'patients': patients})


def add_patient_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient added successfully!")
            return redirect('patients')
    else:
        form = PatientForm()

    return render(request, 'accounts/add_patient.html', {'form': form})


def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient updated successfully!")
            return redirect('patients')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'accounts/edit_patient.html', {
        'form': form,
        'patient': patient
    })


def delete_patient_view(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    messages.success(request, "Patient deleted successfully!")
    return redirect('patients')
from .models import Doctor, Appointment
from .forms import DoctorForm, AppointmentForm


# ---------------- DOCTORS ----------------

def doctors_view(request):
    doctors = Doctor.objects.all()
    return render(request, 'accounts/doctors.html', {'doctors': doctors})


def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor added successfully!")
            return redirect('doctors')
    else:
        form = DoctorForm()

    return render(request, 'accounts/add_doctor.html', {'form': form})


# ---------------- APPOINTMENTS ----------------

def appointments_view(request):
    appointments = Appointment.objects.all().order_by('-date')
    return render(request, 'accounts/appointments.html', {'appointments': appointments})


def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('appointments')
    else:
        form = AppointmentForm()

    return render(request, 'accounts/add_appointment.html', {'form': form})