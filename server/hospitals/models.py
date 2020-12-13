from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Hospital(models.Model):
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=1000)
    description = models.TextField(max_length=1000)
    registered_at = models.DateTimeField(default=datetime.now)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True,null=True)

    def __str__(self) -> str:
        return self.name
    


