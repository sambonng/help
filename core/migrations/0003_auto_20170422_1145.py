# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_announcement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='attached',
            field=models.FileField(blank=True, upload_to=b''),
        ),
    ]
