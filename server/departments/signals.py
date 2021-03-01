from django.db.models.signals import post_save
from django.dispatch import receiver
from departments.models import Department
from queues.models import Queue 



@receiver(post_save,sender = Department)
def created_department(sender,instance,created,**kwargs):
    if created:
        queue_name = instance.name.split()
        queue_name = "_".join(queue_name)
        queue = Queue.objects.create(
            name= queue_name,
            department=instance,
            created_by=instance.created_by,
        )
