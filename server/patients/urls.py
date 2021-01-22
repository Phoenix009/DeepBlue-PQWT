from django.urls import path

from . import views

app_name = 'patients'

urlpatterns = [
    path('register/<str:room_name>',views.register_patient, name = 'register_patient'),
    path('verification-message/',views.verification_message, name = 'verification_message'),
    path('verify/', views.verify, name = 'verify_patient'),
]