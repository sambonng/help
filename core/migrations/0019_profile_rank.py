# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_approvalunit_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rank',
            field=models.IntegerField(choices=[(1, '\ub300\uc7a5'), (2, '\uc911\uc7a5'), (3, '\uc18c\uc7a5'), (4, '\uc900\uc7a5'), (5, '\ub300\ub839'), (6, '\uc911\ub839'), (7, '\uc18c\ub839'), (8, '\ub300\uc704'), (9, '\uc911\uc704'), (10, '\uc18c\uc704'), (11, '\uc900\uc704'), (12, '\uc6d0\uc0ac'), (13, '\uc0c1\uc0ac'), (14, '\uc911\uc0ac'), (15, '\ud558\uc0ac'), (16, '\ubcd1\uc7a5'), (17, '\uc0c1\ubcd1'), (18, '\uc77c\ubcd1'), (19, '\uc774\ubcd1')], default=4),
            preserve_default=False,
        ),
    ]
