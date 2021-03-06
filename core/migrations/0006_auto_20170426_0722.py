# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 07:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20170425_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sol_User_rel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Soldier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=100)),
                ('nth', models.IntegerField()),
                ('image', models.ImageField(blank=True, upload_to=b'')),
                ('phone_num', models.CharField(max_length=10)),
                ('superuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SoldierDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('family_info', models.TextField()),
                ('education', models.TextField()),
                ('birth', models.DateTimeField()),
                ('sevice_num', models.CharField(max_length=12)),
                ('major', models.CharField(max_length=15)),
                ('last_desease', models.TextField()),
                ('first_counsel', models.TextField()),
                ('plan', models.TextField()),
                ('emergency_contact', models.CharField(max_length=20)),
                ('soldier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Soldier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sol_user_rel',
            name='soldier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Soldier'),
        ),
        migrations.AddField(
            model_name='sol_user_rel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
