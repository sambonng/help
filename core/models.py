# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=20, null=True)
    phone_num = models.CharField(max_length=20)

    CHOICES = (
        (1,'대장'), (2,'중장'), (3,'소장'), (4,'준장'), (5,'대령'), (6,'중령'),
        (7,'소령'), (8,'대위'), (9,'중위'), (10,'소위'), (11,'준위'), (12,'원사'),
        (13,'상사'), (14,'중사'), (15,'하사'), (16,'병장'), (17,'상병'),
        (18,'일병'), (19,'이병'),
    )

    rank = models.IntegerField(choices = CHOICES, null=True)

    def __unicode__(self):
        return self.name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Soldier(TimeStampedModel):
    superuser = models.ForeignKey(User)
    name = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    nth = models.IntegerField()
    image = models.ImageField(upload_to='image/', blank=True)
    phone_num = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class SoldierDetail(TimeStampedModel):
    soldier = models.OneToOneField(Soldier, on_delete=models.CASCADE)
    family_info = models.TextField()
    education = models.TextField()
    birth = models.DateField()
    service_num = models.CharField(max_length=12)
    major = models.CharField(max_length=15)
    last_desease = models.TextField()
    first_counsel = models.TextField()
    plan = models.TextField()
    emergency_contact = models.CharField(max_length=20)


class Sol_User_rel(TimeStampedModel):
    soldier = models.ForeignKey(Soldier)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('soldier', 'user',)

    def __unicode__(self):
        return self.soldier.name


class Announcement(TimeStampedModel):
    user = models.ForeignKey(User)
    importance = models.BooleanField(default=False)
    title = models.CharField(max_length=20)
    contents = models.TextField()
    attached = models.FileField(upload_to='documents/', blank=True)

    def __unicode__(self):
        return self.title


class Counsel(TimeStampedModel):
    user = models.ForeignKey(User)
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    date = models.DateField()
    contents = models.TextField()
    plan = models.TextField()
    attached = models.FileField(upload_to='counsels/', blank=True)


class Approval(models.Model):
    counsel = models.OneToOneField(Counsel, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    is_approved = models.NullBooleanField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()
    n1 = models.ForeignKey(User, related_name='n1')
    n2 = models.ForeignKey(User, related_name='n2', null=True)
    n3 = models.ForeignKey(User, related_name='n3', null=True)
    n4 = models.ForeignKey(User, related_name='n4', null=True)
    n5 = models.ForeignKey(User, related_name='n5', null=True)


class ApprovalUnit(models.Model):
    user = models.ForeignKey(User)
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    is_approved = models.NullBooleanField(null=True)
    completed_date = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
#     comments = models.TextField(null=True)

    def __unicode__(self):
        return self.user.profile.name

