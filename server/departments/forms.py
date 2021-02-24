from django import forms
from .models import Department


class DepartmentCreationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "description"]
