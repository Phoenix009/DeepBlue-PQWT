from django import forms
from django.db.models import fields

from . models import Patient

class PatientRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    
