# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20170425_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='importance',
            field=models.BooleanField(default=False),
        ),
    ]
