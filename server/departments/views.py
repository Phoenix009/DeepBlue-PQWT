import json
from .forms import DepartmentCreationForm 

from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.contrib import messages

from departments.models import Department

@login_required
def view_departments(request):
    """
    Can view all the departments in a hospital 
    """
    dept = get_object_or_404(Department, pk=request.user.profile.department.pk)
    departments = dept.get_all_department_in_hospital()
    context={'departments': departments}
    return render(request, 'departments/view_departments.html', context)

@login_required 
def reorder_departments(request):
    """
    Reorders the order of department
    """
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
