from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from hospitals.models import Hospital

class Department(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True,blank=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    order = models.IntegerField(null=True, blank=True)
    group = models.CharField(max_length=255 ,null=True, blank=True)

    def get_queues(self):
        return self.queue_set.all()

    def get_all_department_in_hospital(self):
        hospital = self.hospital
        departments = hospital.department_set.all().order_by('order')
        return departments

    def __str__(self) -> str:
        return f"{self.hospital.name} - > {self.name}"
