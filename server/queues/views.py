import json
from datetime import datetime

from django.contrib.auth import login
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import PermissionDenied
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from qr_code.qrcode.utils import QRCodeOptions

from patients.models import Patient
from queues.models import Queue,VirtualQueue
from patients.forms import PatientRegistrationForm, AdminPatientRegistrationForm
from departments.models import Department

from .utils import update_model

@login_required
def index(request):
    try:
        dept = get_object_or_404(Department, pk = request.user.profile.department.pk)
    except:
        return HttpResponse('You are not assigned to any departments')
        
    # queues = dept.get_queues()
    queues = Queue.get_all_queues_of_hospital(dept.hospital)
    # patients_visited_today = Patient.total_number_of_patients_today()
    first_queue = dept.queue_set.first()
    if first_queue:
        average_wait_time =first_queue.get_waittime()
    else:
        average_wait_time = 0 
    active_patients = VirtualQueue.get_active_patients()
    bounce_rate = VirtualQueue.get_bounce_rate()
    unique_patients = Patient.get_total_number_of_patients()
    context={
        'queues': queues, 
        'department': dept,
        'average_wait_time' : average_wait_time,
        'active_patients' : active_patients,
        'unique_patients' : unique_patients,
        'bounce_rate' : bounce_rate,

        # 'patients_visited_today' : patients_visited_today,
        }
    return render(request, 'queues/index.html', context)

# can be viewed by the queue receptionist 
# displays all the verified patients in the queue 
@login_required
def room(request, room_name):
    queue = Queue.get_queue_by_name(name = room_name)
    if (not request.user.profile.is_superuser) and  (not request.user.profile.department == queue.department ):
        raise PermissionDenied
    if not queue:
        return HttpResponse('does no exist')
    # previous_queue = queue.get_previous_queue()
    
    form = AdminPatientRegistrationForm()
    context = {
        'room_name':room_name, 
        'queue':queue, 
        'form':form,
        # 'previous_queue':previous_queue,
    }
    return render(request, 'queues/queue.html', context)

# shows the wait-time for a patient after he/she clicks on 
# the link sent in email and also verifies the patient 

def view_wait_time(request,token):
    print(token)
    patient = get_object_or_404(Patient, otp = token)
    queues = patient.virtualqueue_set.filter(treatment_completed_at=None,completed_at=None,removed_at=None)
    print(queues)
    if not len(queues):
        context = {
            'patient' : patient,
        }
        return render(request,'queues/out_of_queue.html', context)
    depts = Department.objects.all()
    # queues = Queue.objects.all()
    # queues.sort( key =lambda x : x.department.order)
    patient.verified = True 
    patient.save()
    queue = patient.get_current_queue()
    all_queues = queue.get_all_queues_of_hospital(queue.department.hospital)

    context = {
        'patient' : patient,
        'queue' : queue,
        'vqueue_patient_id' : patient.get_current_queue_id(),
        'all_queues' : all_queues
    }
    return render(request,'queues/view_wait_time.html', context)



# adds a new patient to the queue
@login_required
def add_patient(request,room_name):
    if request.method == 'POST':
        form = AdminPatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = Patient(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data.get('email'),
                phone_number = form.cleaned_data.get('phone_number'),
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
    OUT_OF_QUEUE = 'OUT_OF_QUEUE'
    OUT_OF_SYSTEM = 'OUT_OF_SYSTEM'
    if request.method == 'POST':
        data = json.loads(request.body)
        vqueue_id = data['id']
        room_name = data['room_name']
        type_ = data['type']
        vqueue = get_object_or_404(VirtualQueue, pk = vqueue_id)
        if type_ == OUT_OF_QUEUE:
            vqueue.completed_at = datetime.now()
            send_update_notification(vqueue.queue.name)
        elif type_ == OUT_OF_SYSTEM:
            vqueue.treatment_completed_at = datetime.now()
            hospital = vqueue.queue.department.hospital 
            department_order = vqueue.queue.department.order
            next_order = department_order + 1
            department = hospital.department_set.filter(order = next_order).first()
            if department:
                queue = department.queue_set.first()
                new_vqueue = VirtualQueue(queue = queue, patient = vqueue.patient)
                new_vqueue.save()
                send_update_notification(queue.name)
        vqueue.save()
        update_model(vqueue)
        send_update_notification(room_name)
        return JsonResponse({'status': 'success'})

# Generates and opens qrcode
@login_required
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
    return render(request,'queues/view_wait.html', context)

def token_visualizer(request, pk):
    queue = get_object_or_404(Queue , pk = pk )
    context = {
        'room_name' : queue.name
    }
    return render(request, 'queues/token_visualizer.html', context)

@login_required
def stats(request):
    if not request.user.profile.is_superuser:
        raise PermissionDenied
    queue_data = VirtualQueue.get_comparison()
    hospital = request.user.profile.department.hospital 
    departments = hospital.department_set.all()
    queues = []
    for department in departments:
        queues.extend(list(department.queue_set.all()))
    departments = {}
    for queue in queues:
        departments[queue.name] = VirtualQueue.get_comparison_by_department(queue)
    context = {
        'queue_data' : queue_data,
        'departments' : departments
    }
    return render(request, 'queues/stats.html', context)

