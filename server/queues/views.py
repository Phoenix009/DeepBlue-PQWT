import json
from datetime import datetime

from django.contrib.auth import login
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from qr_code.qrcode.utils import QRCodeOptions

from patients.models import Patient
from queues.models import Queue,VirtualQueue
from patients.forms import PatientRegistrationForm
from departments.models import Department

from .utils import update_model

# displays all the queues in a particular department
@login_required
def index(request):
    dept = get_object_or_404(Department, pk=request.user.profile.department.pk)
    queues = dept.get_queues()
    context={'queues': queues, 'department': dept}
    return render(request, 'queues/index.html', context)

# can be viewed by the queue receptionist 
# displays all the verified patients in the queue 
def room(request, room_name):
    queue = Queue.get_queue_by_name(name = room_name)
    if not queue:
        return HttpResponse('does no exist')
    
    form = PatientRegistrationForm()
    context = {'room_name':room_name, 'queue':queue, 'form':form}
    return render(request, 'queues/queue.html', context)

# shows the wait-time for a patient after he/she clicks on 
# the link sent in email and also verifies the patient 
def view_wait_time(request,token):
    print(token)
    patient = get_object_or_404(Patient, otp = token)
    patient.verified = True 
    patient.save()
    queue = patient.get_current_queue()
    context = {
        'patient' : patient,
        'queue' : queue,
    }
    return render(request,'queues/view_wait_time.html', context)



# adds a new patient to the queue
@login_required
def add_patient(request,room_name):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = Patient(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                age = form.cleaned_data['age'],
                gender = form.cleaned_data['gender'],
                verified=True,
                added_by = request.user
            )
            patient.save()
            queue = Queue.get_queue_by_name(name=room_name)
            inqueue = VirtualQueue(patient=patient, queue=queue)
            inqueue.save()
            send_update_notification(room_name)
    return redirect('queues:room', room_name)


# def get_patients_data(request):
#     data = json.loads(request.body)
#     queue_id = data['queueId']
#     queue = get_object_or_404(Queue, pk = queue_id)
#     patients = queue.get_active_patients()
#     json_context = None 
#     if patients:
#         json_context = serializers.serialize('json', patients) 
#     context = {
#         'data' : json_context
#     }
#     return HttpResponse(json_context, content_type='application/json')

# removes patients from the queue
@login_required
def remove_patient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vqueue_id = data['id']
        room_name = data['room_name']
        vqueue = get_object_or_404(VirtualQueue, pk = vqueue_id)
        vqueue.removed_at = datetime.now()
        vqueue.save()
        send_update_notification(room_name)
        return JsonResponse({'status': 'success'})

# removes patients from the queue for treatment
@login_required
def complete_patient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vqueue_id = data['id']
        room_name = data['room_name']
        vqueue = get_object_or_404(VirtualQueue, pk = vqueue_id)
        vqueue.completed_at = datetime.now()
        vqueue.save()
        update_model(vqueue)
        send_update_notification(room_name)
        return JsonResponse({'status': 'success'})

# Generates and opens qrcode
def open_qrcode(request, room_name):
    qrcode_options = QRCodeOptions(size='H', border=1, error_correction='L')
    context = {
        'qrcode_options' : qrcode_options,
        'room_name' : room_name,
        'qrcode_text': f"http://localhost:8000/patients/register/{room_name}"
    }
    return render(request, 'queues/open_qrcode.html', context = context)

# sends notification to update table
def send_update_notification(room_name):
    group_name = f'chat_{room_name}'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {"type": "update_table"})

# demo view to test ui
def test_ui(request):
    context = {}
    return render(request,'queues/test.html', context)



