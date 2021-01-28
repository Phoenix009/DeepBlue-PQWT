from datetime import datetime
import random
import string 

from django.db import models
from django.contrib.auth.models import User

from departments.models import Department
from patients.models import Patient

class Queue(models.Model):
    name = models.CharField(max_length=500)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,blank=True, null=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    model = models.FileField(upload_to='models/', default='models/default.sav')


    def __str__(self) -> str:
        return self.name
    
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
        
        
    
    def get_active_patients(self):
        return self.virtualqueue_set.filter(treatment_completed_at = None, removed_at=None).all()
    
    def get_active_patients_count(self):
        return len(self.get_active_patients())



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

