from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, UserProfile
from django.core.exceptions import ValidationError

def my_view(request):
    return render(request, 'index.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            return render(request, 'index.html', {'error': 'All fields are required.'})

        send_mail(
            subject=f'Message from {name}',
            message=message,
            from_email=email,
            recipient_list=['your_email@example.com'],
        )
        return redirect('contact_success')

    return render(request, 'index.html')

def contact_success_view(request):
    return render(request, 'contact_success.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')

        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        try:
            UserProfile.objects.create(user=user, phone=phone, date_of_birth=date_of_birth)
        except ValidationError as e:
            return render(request, 'register.html', {'error': str(e)})

        auth_login(request, user)
        return redirect('dashboard')  # Redirect to dashboard after successful registration

    return render(request, 'register.html')

def logout_view(request):
    auth_logout(request)
    return redirect('my_view')

@login_required
def schedule_appointment_view(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')

        appointment = Appointment(
            user=request.user,
            date=date,
            time=time,
            description=description
        )
        appointment.save()

        messages.success(request, 'Your appointment has been scheduled successfully!')
        return redirect('appointment_confirmation')  # Redirect to confirmation page

    return render(request, 'schedule_appointment.html')

def appointment_confirmation_view(request):
    return render(request, 'appointment_confirmation.html')

@login_required
def dashboard_view(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user)
    # Show different content based on whether the user has appointments
    return render(request, 'dashboard.html', {'appointments': appointments})
