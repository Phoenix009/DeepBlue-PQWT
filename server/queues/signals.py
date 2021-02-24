from django.db.models.signals import pre_save
from django.dispatch import receiver
from departments.models import Department
from queues.models import Queue 
from django.core.files import File
import os

@receiver(pre_save,sender = Queue)
def save_queue(sender,instance,**kwargs):
    local_file = open(os.path.join('core', 'static', 'models', 'model.sav'), 'rb')
    django_file = File(local_file)
    django_file.name = "model.sav"
    instance.model = django_file
    # local_file.close()

