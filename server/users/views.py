from django.contrib.auth.forms import UsernameField
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied


from patients.utils import generate_otp
from hospitals.models import Hospital
from users.forms import StaffCreationForm, ProfileCreationForm
from users.models import Profile
from departments.models import Department
from users.utils import send_staff_registration_mail

@login_required
def view_staff(request, pk):
    if not request.user.profile.is_superuser:
        raise PermissionDenied
    hospital = get_object_or_404(Hospital, pk=pk)
    staff_list = hospital.get_staff()
    context = {
        'hospital': hospital, 
        'staff_list': staff_list
    }
    return render(request, 'users/view_staff.html', context)

@login_required
def create_staff(request, pk):
    if not request.user.profile.is_superuser:
        raise PermissionDenied
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
            user = User.objects.create_user(
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
            send_staff_registration_mail(staff=user.profile, password=password, admin_email=request.user.email)
            messages.success(request, "Staff Created Successfully !")
            return redirect('users:view_staff', hospital.pk)
        else:
            messages.error(request, "Staff Creation Failed !")

    context = {
        'staff_creation_form': staff_creation_form,
        'profile_creation_form': profile_creation_form,
    }

    return render(request, 'users/staff_creation.html', context)