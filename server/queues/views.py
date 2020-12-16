import json

from django.contrib.auth import login
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from patients.models import Patient
from queues.models import Queue,VirtualQueue

def index(request):
    context = {}
    return render(request, 'index.html', context)


def room(request, room_name):
    context = {'room_name':room_name}
    return render(request, 'queue.html', context)


def add_patient(request,room_name):
    print('here1')
    data = json.loads(request.body)
    queue_id = data['queueId']
    queue = get_object_or_404(Queue, pk = queue_id)
    email = data['email']
    first_name = data['firstName']
    last_name = data['lastName']
    verified = True 
    patient = Patient(
        first_name = first_name, 
        last_name = last_name, 
        email = email, 
        verified=verified, 
        added_by = request.user 
    )
    patient.save()
    virtual_queue = VirtualQueue(patient = patient, queue = queue)
    virtual_queue.save()
    print('here2')
    return JsonResponse({'added':'ok'})

    
