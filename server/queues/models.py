from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from departments.models import Department
from patients.models import Patient

class Queue(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)

class VirtualQueue(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.queue.name} -> {self.patient.email}"