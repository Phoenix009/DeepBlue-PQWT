# Generated by Django 3.1.2 on 2020-12-18 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualqueue',
            name='joined_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
