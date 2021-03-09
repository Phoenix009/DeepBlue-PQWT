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

    def get_departments(self):
        return list(self.department_set.all())
    
    def get_staff(self):
        dept_list = self.get_departments()
        print(dept_list)
        staff_list = []
        for dept in dept_list:
            staff_list.extend(list(dept.profile_set.all()))
        print(staff_list)
        return staff_list
