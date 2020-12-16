from departments.models import Department
from django.shortcuts import get_object_or_404, render


def view_queues(request):
    dept = get_object_or_404(Department, pk=request.user.profile.department.pk)
    queues = dept.get_queues()
    context={'queues': queues, 'department': dept}
    return render(request, 'departments/view_queues.html', context)
