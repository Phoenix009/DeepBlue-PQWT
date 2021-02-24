from django.db.models.signals import post_save
from django.dispatch import receiver
from departments.models import Department
from queues.models import Queue 



@receiver(post_save,sender = Department)
def created_department(sender,instance,created,**kwargs):
    if created:
        queue = Queue.objects.create(
            name=instance.name,
            department=instance,
            created_by=instance.created_by,
        )
