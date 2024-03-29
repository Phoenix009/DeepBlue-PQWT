from datetime import datetime , date
import random
import string 

from django.db import models
from django.contrib.auth.models import User

from departments.models import Department
from patients.models import Patient
from .utils import predict_waittime

class Queue(models.Model):
    name = models.CharField(max_length=500)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,blank=True, null=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    model = models.FileField(upload_to='models/', default='models/default.sav')
    max_limit = models.IntegerField(default=20,null=True,blank=True)


    def __str__(self) -> str:
        return f"{self.name} -> {self.department.hospital}"

    @property
    def get_queue_name(self):
        return self.department.name

    @classmethod
    def get_queue_by_name(cls,name):
        queue = cls.objects.filter(name=name).first()
        return queue
    
    def get_previous_queue(self):
        previous_order = self.department.order -1 
        if previous_order >= 1:
            dept = Department.objects.filter(order = previous_order).first()
            return Queue.objects.filter(department = dept).first().name 
    
    def get_next_queue(self):
        next_queue = self.department.order + 1 
        dept = Department.objects.filter(order = next_queue).first()
        if dept:
            return Queue.objects.filter(department = dept).first()
    
    def get_waittime(self):
        vqueue = list(self.virtualqueue_set.exclude(treatment_completed_at=None).all())
        vqueue = vqueue[-10:]
        total_waittime = sum(map(lambda x: (x.completed_at - x.joined_at).seconds//60, vqueue ))
        return total_waittime // max(1, len(vqueue))


    def get_active_patients(self):
        return self.virtualqueue_set.filter(treatment_completed_at = None, removed_at=None).all()
    
    def get_active_patients_count(self):
        return len(self.get_active_patients())

    @property
    def get_progress_bar_status(self):
        return min(100, int(self.get_active_patients_count() / self.max_limit * 100))
    
    def get_previous_queues(self):
        dept = self.department
        dept_list = list(Department.objects.filter(order__lt = dept.order))[:3]
        queues = list(map(lambda dept: dept.queue_set.first(), dept_list))
        return queues

    def get_next_queues(self):
        dept = self.department
        dept_list =  list(Department.objects.filter(order__gt = dept.order))[:3]
        queues = list(map(lambda dept: dept.queue_set.first(), dept_list))
        return queues

    @classmethod
    def get_all_queues_of_hospital(cls,hospital):
        departments = hospital.department_set.all().order_by('order')
        queues = []
        for dept in departments:
            queues.extend([ queue for queue in dept.queue_set.all() ])
        return queues 

        
class VirtualQueue(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=datetime.now)
    removed_at = models.DateTimeField(default=None,null=True,blank=True)
    treatment_completed_at = models.DateTimeField(default = None, null=True,blank=True)
    completed_at = models.DateTimeField(default=None,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.queue.name} -> {self.patient.email}"
    
    def wait_time(self):
        if not self.completed_at: return -1
        else: return (self.completed_at.hour*60 + self.completed_at.minute) - (self.joined_at.hour*60 + self.joined_at.minute)

    @classmethod
    def get_comparison(cls):
        completion = 12
        data = []
        vqueue = cls.objects.all()
        for vq in vqueue:
            predicted_wait_time, completion = predict_waittime(vq, completion)
            actual_wait_time = vq.wait_time()
            if actual_wait_time == -1:
                continue
            data.append({
                'id' : vq.id ,
                "predicted_wait_time" : int(predicted_wait_time),
                "actual_wait_time" : actual_wait_time, 
            })
        
        return data 
    
    @classmethod
    def get_comparison_by_department(cls , queue):
        completion = 12
        data = []
        vqueue = cls.objects.filter(queue = queue).all()
        for vq in vqueue:
            predicted_wait_time, completion = predict_waittime(vq, completion)
            actual_wait_time = vq.wait_time()
            if actual_wait_time == -1:
                continue
            data.append({
                'id' : vq.id ,
                "predicted_wait_time" : int(predicted_wait_time),
                "actual_wait_time" : actual_wait_time, 
            })
        
        return data



    def get_patients_ahead(self):
        '''
            Returns the number of patient ahead of the patient in the queue
        '''

        active_patients = self.queue.get_active_patients()
        print(active_patients)
        count = 0
        for patient in active_patients:
            if patient.patient.id == self.patient.id: return count
            count += 1
        else:
            return -1

    @classmethod
    def get_active_patients(cls):
        return len(cls.objects.filter(treatment_completed_at=None, removed_at = None).all())
    
    @classmethod
    def get_bounce_rate(cls):
        vqueue  = cls.objects.filter(joined_at__startswith=date.today())
        total_serviced = len(vqueue.filter(removed_at = None))
        total_in_queue = len(vqueue)
        if not total_in_queue:
            return 0 
        return round(((total_in_queue - total_serviced)/total_in_queue)*100, 2) 

