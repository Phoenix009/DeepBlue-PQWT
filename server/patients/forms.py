from django import forms
from django.db.models import fields

from . models import Patient

class PatientRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('TRANS', 'TRANS'),
    ])

class VerificationForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField()


class JoinQueueForm(forms.Form):
    email = forms.EmailField()