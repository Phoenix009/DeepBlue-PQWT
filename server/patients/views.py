from datetime import datetime
from django.shortcuts import get_object_or_404, render,redirect


from hospitals.models import Hospital
from queues.models import Queue, VirtualQueue
from .forms import PatientRegistrationForm, VerificationForm
from .models import Patient
from .utils import send_patient_registration_mail,generate_otp, send_patient_verification_mail
import string
import random

# displays a  form to register the patient after 
# scanning the QRCODE
def register_patient(request, room_name):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            age = form.cleaned_data.get('age')
            gender = form.cleaned_data.get('gender')
            otp = generate_otp()
            patient = Patient(
                first_name = first_name,
                last_name = last_name,
                email = email,
                otp = otp,
                age = age,
                gender = gender,
            )
            patient.save()
            queue = Queue.get_queue_by_name(name= room_name)
            inqueue = VirtualQueue(queue = queue, patient=patient)
            inqueue.save()
            send_patient_registration_mail(patient)
            return redirect('patients:verification_message')
    else:
        form = PatientRegistrationForm()
    context = {
        'form':form,
        'room_name' : room_name
    }
    return render(request, 'patients/register_patient.html', context)

def verification_message(request):
    context = {}
    return render(request, 'patients/verification_message.html', context)



# Not being used 
# registeres the patient after he/she enters the otp sent 
# in email 
def verify(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.filter(email=form.cleaned_data['email'], verified=False).first()
            print(patient)
            if not patient:
                return redirect('patients:register_patient')
            if patient.otp == form.cleaned_data['otp']:
                patient.verified = True
                patient.save()
                queue_name = patient.get_queue_name
                queue_link = f"http://localhost:8000/queue/{queue_name}"
                send_patient_verification_mail(patient, queue_link)
    else:
        form = VerificationForm()
    context = {'form': form}
    return render(request, 'patients/verify.html', context)


def view_patients(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    patients = Patient.get_patients_today()
    context = {
        'patients': patients,
        'hopsital': hospital,
    }

    return render(request, 'patients/view_patients.html', context)
