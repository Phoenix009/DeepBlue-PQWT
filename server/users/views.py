from django.contrib.auth.forms import UsernameField
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from patients.utils import generate_otp
from hospitals.models import Hospital
from users.forms import StaffCreationForm, ProfileCreationForm
from users.models import Profile
from departments.models import Department


@login_required
def view_staff(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    staff_list = hospital.get_staff()
    context = {
        'staff_list': staff_list
    }
    return render(request, 'users/view_staff.html', context)

def create_staff(request, pk):
    
    hospital = get_object_or_404(Hospital, pk=pk)
    if request.method == 'GET':
        staff_creation_form = StaffCreationForm()
        profile_creation_form = ProfileCreationForm(hospital)
    else:
        staff_creation_form = StaffCreationForm(request.POST)
        profile_creation_form = ProfileCreationForm(hospital, request.POST)
        if staff_creation_form.is_valid() and profile_creation_form.is_valid():
            data = {**staff_creation_form.cleaned_data, **profile_creation_form.cleaned_data}
            department = get_object_or_404(Department, pk=int(data.get('department')))
            password = generate_otp(k=8)
            print('Password:', password)
            user = User(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                username=data.get('username'),
                password = password,
                is_active = True
            )
            user.save()
            user.profile.department = department
            user.profile.is_incharge = data.get('is_incharge')
            user.profile.is_superuser = data.get('is_superuser')
            user.profile.save()
            messages.success(request, "Staff Created Successfully !")
            return redirect(request, 'users:view_staff')
        else:
            messages.error(request, "Staff CreationFailed !")

    context = {
        'staff_creation_form': staff_creation_form,
        'profile_creation_form': profile_creation_form,
    }

    return render(request, 'users/staff_creation.html', context)