from django.core.mail import send_mail 
import random
import string

def send_patient_registration_mail(patient):
    subject = 'Patient Registraion OTP'
    body = f"""
    You are one step away from getting into the queue 
    Login using the following credentials
    Email : {patient.email}
    Password : {patient.otp}
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