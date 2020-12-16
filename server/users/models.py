from departments.models import Department
from django.db import models
from django.contrib.auth.models import User 

from departments.models import Department


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_incharge = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} Profile'

    