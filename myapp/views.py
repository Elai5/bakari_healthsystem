# this is just a comment to guide you. start with the info.py, then the views.py. everything else is set.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.contrib.auth import login
# Existing views
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

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('my_view')  # Redirect to home or any other page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Register view
def register_view(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')

        # Validate password confirmation
        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})

        # Create the user
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        # Save additional user profile data
        try:
            UserProfile.objects.create(user=user, phone=phone, date_of_birth=date_of_birth)
        except ValidationError as e:
            # Handle validation error if needed
            return render(request, 'register.html', {'error': str(e)})

        # Log the user in and redirect to login page
        login(request, user)
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'register.html')
# Logout view
def logout_view(request):
    auth_logout(request)
    return redirect('my_view')  # Redirect to home or any other page


@login_required
def schedule_appointment_view(request):
    if request.method == 'POST':
        # Retrieve data from the form
        date = request.POST.get('date')
        time = request.POST.get('time')
        description = request.POST.get('description')
        
        # Create and save the appointment
        appointment = Appointment(
            user=request.user,
            date=date,
            time=time,
            description=description
        )
        appointment.save()
        
        # Show a success message and redirect to a confirmation page
        messages.success(request, 'Your appointment has been scheduled successfully!')
        return redirect('appointment_confirmation')  # Make sure this view exists

    return render(request, 'schedule_appointment.html')


def appointment_confirmation_view(request):
    return render(request, 'appointment_confirmation.html')
