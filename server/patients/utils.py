from django.core.mail import send_mail 
import random
import string

def send_patient_registration_mail(patient):
    subject = 'Patient Registraion OTP'
    body = f"""
    You are one step away from getting into the queue 
    Click on the link to enter the queue
    Email : {patient.email}
    http://localhost:8000/queues/patients/wait-time/{patient.otp}/
    """
    sender = 'stationeymanagerkjsieit@gmail.com'
    receiver = patient.email 
    send_mail(
        subject,
        body,
        sender,
        [receiver,],
        fail_silently=False
    )

def send_patient_verification_mail(patient, queue_link):
    subject = 'Patient Verified'
    body = f"""
    You have been verified!
    Head over to this link to join the queue:
    {queue_link}
    """
    sender = 'stationeymanagerkjsieit@gmail.com'
    receiver = patient.email 
    send_mail(
        subject,
        body,
        sender,
        [receiver,],
        fail_silently=False
    )

def generate_otp():
    return "".join(random.choices(string.ascii_uppercase, k=6))