from django.shortcuts import render,redirect


from .forms import PatientRegistrationForm
from .models import Patient
from .utils import send_patient_registration_mail,generate_otp
import string
import random

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            otp = generate_otp()
            patient = Patient(
                first_name = first_name,
                last_name = last_name,
                email = email,
                otp = otp, 
            )  
            patient.save()
            send_patient_registration_mail(patient)
    else:
        form = PatientRegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'patients/register_patient.html', context)

