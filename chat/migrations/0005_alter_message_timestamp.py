# Generated by Django 4.2.9 on 2024-02-09 11:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_message_delete_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 9, 16, 38, 36, 352350)),
        ),
    ]
