import json

from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from django.core import serializers

from patients.models import Patient
from queues.models import Queue,VirtualQueue

def index(request):
    context = {}
    return render(request, 'index.html', context)


def room(request, room_name):
    queue = Queue.get_queue_by_name(name = room_name)
    if not queue:
        return HttpResponse('does no exist')
    context = {'room_name':room_name, 'queue':queue}
    return render(request, 'queues/queue.html', context)


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
    
    
