from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields= ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', ]


class ProfileCreationForm(forms.Form):
    def __init__(self, hospital, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(*args,**kwargs)
        dept_list = hospital.get_departments()
        self.fields['department'].choices = [(dept.id, dept) for dept in dept_list]
    
    is_incharge = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    department = forms.ChoiceField()



class StaffCreationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields= ['first_name', 'last_name', 'username', 'email']

