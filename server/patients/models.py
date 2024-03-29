import datetime
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_otp



class Patient(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(null=True, blank=True, max_length=10)
    otp = models.CharField(max_length=20, default=generate_otp ,unique=True)
    joined_at = models.DateTimeField(default=datetime.datetime.now)
    verified = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, default=None,null=True,blank=True, on_delete=models.CASCADE)

    @property
    def get_queue_name(self):
        return self.virtualqueue_set.first().queue.name
    
    @property
    def get_virtual_queue(self):
        return self.virtualqueue_set.first()
    
    def get_current_queue(self):
        vqueue =  self.virtualqueue_set.filter(treatment_completed_at=None).first()
        if vqueue:
            return vqueue.queue 
        return None 
    
    def get_current_queue_id(self):
        return self.virtualqueue_set.filter(treatment_completed_at=None, removed_at = None).first().id 
    
    @classmethod
    def get_total_number_of_patients(cls):
        return len(cls.objects.all())


    @classmethod
    def get_patients_today(cls):
        return cls.objects.filter(joined_at__gte=datetime.date.today()).order_by('-joined_at')


    def __str__(self) -> str:
        return f"{self.id} {self.first_name} {self.last_name}"
    
