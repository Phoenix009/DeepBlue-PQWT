from django.shortcuts import get_object_or_404, render,redirect


from queues.models import Queue, VirtualQueue
from .forms import PatientRegistrationForm, VerificationForm
from .models import Patient
from .utils import send_patient_registration_mail,generate_otp, send_patient_verification_mail
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
            queue = Queue.get_queue_by_name(name='room')
            inqueue = VirtualQueue(queue = queue, patient=patient)
            inqueue.save()
            send_patient_registration_mail(patient)
    else:
        form = PatientRegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'patients/register_patient.html', context)


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

