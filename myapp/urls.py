from django.urls import path
from . import views
from .views import dashboard_view

urlpatterns = [
    path('', views.my_view, name='my_view'),
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success_view, name='contact_success'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('schedule/', views.schedule_appointment_view, name='schedule_appointment'),
    path('appointment-confirmation/', views.appointment_confirmation_view, name='appointment_confirmation'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('quick-contact/', views.quick_contact_view, name='quick_contact'),
]

