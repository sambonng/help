# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 11:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20170506_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approval',
            name='counsel',
        ),
        migrations.RemoveField(
            model_name='approval',
            name='n1',
        ),
        migrations.RemoveField(
            model_name='approval',
            name='n2',
        ),
        migrations.RemoveField(
            model_name='approval',
            name='n3',
        ),
        migrations.RemoveField(
            model_name='approval',
            name='n4',
        ),
        migrations.RemoveField(
            model_name='approval',
            name='n5',
        ),
        migrations.RemoveField(
            model_name='approvalunit',
            name='approval',
        ),
        migrations.RemoveField(
            model_name='approvalunit',
            name='user',
        ),
        migrations.DeleteModel(
            name='Approval',
        ),
        migrations.DeleteModel(
            name='ApprovalUnit',
        ),
    ]
