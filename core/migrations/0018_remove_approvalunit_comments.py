# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 11:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_approval_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvalunit',
            name='comments',
        ),
    ]