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


    def __str__(self) -> str:
        return f"{self.hospital.name} - > {self.name}"
    
class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.department.name} -> {self.user.name}"


    