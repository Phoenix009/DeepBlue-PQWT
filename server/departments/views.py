import json 

from django.shortcuts import get_object_or_404, render
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

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
