from django.urls import path

from . import views

app_name = 'patients'

urlpatterns = [
    path('register/',views.register_patient, name = 'register_patient'),
]