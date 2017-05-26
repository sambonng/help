# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from core.models import(
    Profile, Announcement, Soldier, SoldierDetail, Counsel,
)

class SignUpForm(UserCreationForm):
    name = forms.CharField()
    department = forms.CharField()
    phone_num = forms.CharField()

    CHOICES = (
        (1,'대장'), (2,'중장'), (3,'소장'), (4,'준장'), (5,'대령'), (6,'중령'),
        (7,'소령'), (8,'대위'), (9,'중위'), (10,'소위'), (11,'준위'), (12,'원사'),
        (13,'상사'), (14,'중사'), (15,'하사'), (16,'병장'), (17,'상병'),
        (18,'일병'), (19,'이병'),
    )

    rank = forms.ChoiceField(choices = CHOICES)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'department',
                  'phone_num','rank')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('rank', 'name', 'department', 'position', 'phone_num', )


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'importance', 'contents', 'attached', )


class SoldierForm(forms.ModelForm):
    class Meta:
        model = Soldier
        fields = ('name', 'department', 'nth', 'image', 'phone_num', )


class SoldierDetailForm(forms.ModelForm):
    class Meta:
        model = SoldierDetail
        fields = ('family_info', 'education', 'birth', 'service_num', 'major',
                 'last_desease', 'first_counsel', 'plan', 'emergency_contact', )


class CounselForm(forms.ModelForm):
    n1 = forms.IntegerField()
    n2 = forms.IntegerField(required = False)
    n3 = forms.IntegerField(required = False)
    n4 = forms.IntegerField(required = False)
    n5 = forms.IntegerField(required = False)
    class Meta:
        model = Counsel
        fields = ('date', 'contents', 'plan', 'attached',
                  'n1', 'n2', 'n3', 'n4', 'n5',)
