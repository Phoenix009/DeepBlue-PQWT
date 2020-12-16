from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    joined_at = models.DateTimeField(default=datetime.now)
    verified = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, default=None,null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.email}"
