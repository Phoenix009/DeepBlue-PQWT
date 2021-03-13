import json
from .forms import DepartmentCreationForm 

from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from departments.models import Department

@login_required
def view_departments(request):
    """
    Can view all the departments in a hospital 
    """
    if not request.user.profile.is_superuser:
        raise PermissionDenied
    dept = get_object_or_404(Department, pk=request.user.profile.department.pk)
    departments = dept.get_all_department_in_hospital()
    context={'departments': departments}
    return render(request, 'departments/view_departments.html', context)

@login_required 
def reorder_departments(request):
    """
    Reorders the order of department
    """
    if not request.user.profile.is_superuser:
        raise PermissionDenied
    try:
        departments = []
        new_department_orders = json.loads(request.body)
        print(new_department_orders)
        for new_order in new_department_orders:
            order = new_order['order']
            pk = new_order['pk']
            dept = get_object_or_404(Department , pk = pk)
            dept.order = order 
            departments.append(dept)
        for dept in departments:
            dept.save()
    except Exception as e:
        print(e)
        JsonResponse({'reorderd':'false'})
    return JsonResponse({'reorderd':'ok'})


@login_required
def create_department(request):
    if not request.user.profile.is_superuser:
        raise PermissionDenied
    form = DepartmentCreationForm()
    if request.method == 'POST':
        form = DepartmentCreationForm(request.POST)
        if form.is_valid():
            hospital = request.user.profile.department.hospital
            max_order_dept = hospital.department_set.all().aggregate(Max('order'))
            print(max_order_dept)
            new_order = 1 if not max_order_dept else max_order_dept['order__max'] + 1
            department = Department(
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                order=new_order,
                hospital=hospital,
                created_by=request.user
            )
            department.save()
            messages.success(request, "Department Created Successfully!")
            return redirect('departments:view_departments')
        else:
            messages.error(request, "Form Details Invalid")
    return render(request, "departments/department_creation.html", {"form": form})

@login_required
def update_department(request, pk):
    if not request.user.profile.is_superuser:
        raise PermissionDenied
    department = get_object_or_404(Department , pk = pk)
    form = DepartmentCreationForm(instance = department)
    if request.method == 'POST':
        form = DepartmentCreationForm(request.POST)
        if form.is_valid():
            department = get_object_or_404(Department , pk = pk)
            department.name = form.cleaned_data.get('name')
            department.description = form.cleaned_data.get('description')
            department.save()
            messages.success(request, "Department Updated Successfully!")
            return redirect('departments:view_departments')
        else:
            messages.danger(request, "Form Details Invalid") 
    context = {
            "form": form,
            "department" : department,
        }
    return render(request, "departments/update_department.html",context)

@login_required
def delete_department(request, pk):
    if not request.user.profile.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        department = get_object_or_404(Department , pk = pk)
        department.delete()
        return redirect('departments:view_departments')