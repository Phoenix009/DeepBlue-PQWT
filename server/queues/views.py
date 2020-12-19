import json

from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from patients.models import Patient
from queues.models import Queue,VirtualQueue
from patients.forms import PatientRegistrationForm
from departments.models import Department

@login_required
def index(request):
    dept = get_object_or_404(Department, pk=request.user.profile.department.pk)
    queues = dept.get_queues()
    context={'queues': queues, 'department': dept}
    return render(request, 'queues/index.html', context)


def room(request, room_name):
    queue = Queue.get_queue_by_name(name = room_name)
    if not queue:
        return HttpResponse('does no exist')
    
    form = PatientRegistrationForm()
    context = {'room_name':room_name, 'queue':queue, 'form':form}
    return render(request, 'queues/queue.html', context)

@login_required
def add_patient(request,room_name):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = Patient(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                verified=True,
                added_by = request.user
            )
            patient.save()
            queue = Queue.get_queue_by_name(name=room_name)
            inqueue = VirtualQueue(patient=patient, queue=queue)
            inqueue.save()
            send_update_notification(room_name)
    return redirect('queues:room', room_name)


def get_patients_data(request):
    data = json.loads(request.body)
    queue_id = data['queueId']
    queue = get_object_or_404(Queue, pk = queue_id)
    patients = queue.get_active_patients()
    json_context = None 
    if patients:
        json_context = serializers.serialize('json', patients) 
    context = {
        'data' : json_context
    }
    return HttpResponse(json_context, content_type='application/json')

def remove_patient(request):
    pass 


def send_update_notification(room_name):
    group_name = f'chat_{room_name}'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {"type": "update_table"})

