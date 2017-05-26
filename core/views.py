# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime

from core.forms import (
    SignUpForm, ProfileForm, AnnouncementForm, SoldierForm, SoldierDetailForm,
    CounselForm
)
from core.models import (
    Profile, Announcement, Soldier, SoldierDetail, Sol_User_rel, Counsel,
    Approval, ApprovalUnit
)

# Create your views here.

# user

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    soldier_list = Soldier.objects.filter(sol_user_rel__user=request.user).order_by('id')[:5]
    announcement_imp = Announcement.objects.filter(importance=True).order_by('-created')[:2]
    announcement_list = Announcement.objects.filter(importance=False).order_by('-created')[:3]
    return render(request, 'index.html', {
        'soldier_list':soldier_list,
        'announcement_imp': announcement_imp,
        'announcement_list': announcement_list,
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print form.data
            user = form.save()
            user.refresh_from_db()
            user.profile.name = form.cleaned_data.get('name')
            user.profile.department = form.cleaned_data.get('department')
            user.profile.position = form.cleaned_data.get('position')
            user.profile.phone_num = form.cleaned_data.get('phone_num')
            user.profile.rank = form.cleaned_data.get('rank')
            user.save()
            messages.success(request, '가입이 완료되었습니다. 로그인 해주십시오.')
            return redirect('login')
        else:
            messages.warning(request, '다시 작성해주십시오.')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request):
    return render(request, 'profile/profile.html', {})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, '비밀번호가 성공적으로 변경되었습니다. 다시 로그인해 주십시오')
            logout(request)
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/profile-change-password.html',
                  {'form': form})

@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('성공적으로 변경되었습니다.'))
            return redirect('home')
        else:
            messages.error(request, _('에러를 확인해 주십시오.'))

    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile/profile-update.html',{'form':form})


# announcement


def announcement_list(request):
    announcement_imp = Announcement.objects.filter(importance=True).order_by('-created')
    announcement_list = Announcement.objects.filter(importance=False).order_by('-created')

    q = request.GET.get("q")
    if q:
        announcement_list = announcement_list.filter(title__icontains=q)

    page = request.GET.get('page', 1)
    paginator = Paginator(announcement_list, 10)
    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)

    return render(request, 'announcement/list.html',
                  {'announcements':announcements,
                  'announcements_imp':announcement_imp})

def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = request.user
            announcement.save()
            messages.success(request, '공지사항 등록이 완료되었습니다.')
            return redirect(reverse('announcement-detail',
                                    kwargs={'pk':announcement.id}))
    else:
        form = AnnouncementForm()
    return render(request, 'announcement/create.html',{'form':form})

def announcement_detail(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    auth = False;
    if request.user == announcement.user:
        auth = True;
    return render(request, 'announcement/detail.html',
                  {'announcement':announcement, 'auth':auth})

def announcement_update(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            messages.info(request, '공지사항 수정이 완료되었습니다.')
            return redirect(reverse('announcement-detail',
                                    kwargs={'pk':announcement.id}))
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcement/create.html',{'form':form})

def announcement_delete(request, pk):
    if request.method == 'POST':
        announcement = Announcement.objects.get(pk=pk)
        announcement.delete()
        messages.info(request, '공지사항 삭제가 완료되었습니다.')
        return redirect('announcement-list')


# soldier

def soldier_list(request):
    soldiers = Soldier.objects.filter(sol_user_rel__user=request.user).all()
    return render(request, 'soldier/list.html', {'soldiers':soldiers})

def soldier_detail(request, pk):
    soldier = Soldier.objects.get(pk=pk)
    auth = False
    if soldier.superuser == request.user:
        auth = True
    detail = SoldierDetail.objects.get(soldier=soldier)
    return render(request, 'soldier/detail.html', {
        'soldier': soldier,
        'detail': detail,
        'auth': auth
    })

def soldier_enroll_user(request, pk):
    soldier = Soldier.objects.get(pk=pk)

    if soldier.superuser != request.user:
        return Http404

    if request.method == 'POST' :
        user_id = request.POST['userid']
        Sol_User_rel.objects.get_or_create(soldier=soldier, user_id=user_id)

    users = User.objects.filter(~Q(sol_user_rel__soldier=soldier))
    cur_users = User.objects.filter(sol_user_rel__soldier=soldier)

    return render(request, 'soldier/enroll.html', {
        'cur_users': cur_users, 'users': users, 'pk': pk})

def ajax_soldier(request, pk):
    name = request.GET.get('name', None)
    users = User.objects.filter(profile__name__icontains=name)

    return render(request, 'soldier/ajaxtable.html', {'users':users, 'pk':pk})


def soldier_create(request):
    if request.method == 'POST':
        form_1 = SoldierForm(request.POST, request.FILES)
        form_2 = SoldierDetailForm(request.POST)
        if form_1.is_valid() and form_2.is_valid():
            soldier = form_1.save(commit=False)
            soldier.superuser = request.user
            soldier.save()
            detail = form_2.save(commit=False)
            detail.soldier = soldier
            detail.save()
            Sol_User_rel.objects.create(soldier=soldier,user=request.user)
            messages.success(request, '병사 등록이 완료되었습니다.')
            return redirect(reverse('soldier-detail',
                                   kwargs={'pk': soldier.id}))
    else:
        form_1 = SoldierForm()
        form_2 = SoldierDetailForm()

    return render(request, 'soldier/create.html', {
            'soldierForm': form_1,
            'detailForm': form_2,
        })

def soldier_update(request, pk):
    soldier = Soldier.objects.get(pk=pk)
    soldier_detail = SoldierDetail.objects.get(soldier=soldier)
    if request.method == 'POST':
        form_1 = SoldierForm(request.POST, request.FILES, instance=soldier)
        form_2 = SoldierDetailForm(request.POST, instance=soldier_detail)
        if form_1.is_valid() and form_2.is_valid():
            form_1.save()
            form_2.save()
            messages.info(request, '병사 수정이 완료되었습니다.')
            return redirect(reverse('soldier-detail',
                                 kwargs={'pk':soldier.id}))
    else:
        form_1 = SoldierForm(instance=soldier)
        form_2 = SoldierDetailForm(instance=soldier_detail)

    return render(request, 'soldier/update.html', {
            'soldierForm': form_1,
            'detailForm': form_2
        })

# counsel

def counsel(request):
    soldier_list = Soldier.objects.filter(sol_user_rel__user=request.user).all()
    return render(request, 'counsel/index.html',{
        'soldiers': soldier_list,
    })

def counsel_list(request, pk):
    counsel_list = Counsel.objects.filter(soldier=pk,approval__is_approved=True).order_by('-date')
    page = request.GET.get('page', 1)

    paginator = Paginator(counsel_list, 10)
    try:
        counsels = paginator.page(page)
    except PageNotAnInteger:
        counsels = paginator.page(1)
    except EmptyPage:
        counsels = paginator.page(paginator.num_pages)

    return render(request,'counsel/list.html', {
        'counsels': counsel_list,
        'pk': pk
    })

def counsel_create(request, pk):
    soldier = Soldier.objects.get(pk=pk)
    if request.method == 'POST':
        form = CounselForm(request.POST, request.FILES)
        if form.is_valid():
            counsel = form.save(commit=False)
            counsel.user = request.user
            counsel.soldier = soldier
            counsel.save()
            count = 1
            approval = Approval.objects.create(
                counsel = counsel, n1_id = form.cleaned_data.get('n1'),
                count = count
            )

            data = form.cleaned_data.get('n2')
            print data
            if data != None:
                approval.n2_id = data
                count = 2

            data = form.cleaned_data.get('n3')
            if data != None:
                approval.n3_id = data
                count = 3

            data = form.cleaned_data.get('n4')
            if data != None:
                approval.n4_id = data
                count = 4

            data = form.cleaned_data.get('n5')
            if data != None:
                approval.n5_id = data
                count = 5

            approval.count = count
            approval.save()

            uid = 'n' + str(count)
            ApprovalUnit.objects.create(
                user_id = form.cleaned_data.get(uid),
                approval = approval,
            )

            messages.success(request, '면담 등록이 완료되었습니다.')
            return redirect('approval')
    else:
        form = CounselForm()
        return render(request, 'counsel/create.html',{
            'form': form, 'pk':soldier.id})

def counsel_create_popup(request, pk):
    users = User.objects.filter(sol_user_rel__soldier_id=pk)
    return render(request, 'counsel/popup.html', {'users': users, 'pk': pk})

def ajax_counsel(request, pk):
    name = request.GET.get('name', None)
    users = User.objects.filter(profile__name__icontains=name,
                                sol_user_rel__soldier=pk)

    return render(request,'counsel/ajaxtable.html', {'users':users})

def counsel_detail(request, pk, pkc):
    counsel = Counsel.objects.get(pk=pkc)
    return render(request, 'counsel/detail.html', {
        'counsel': counsel,
    })

#approval

def approval(request):
    approval_req = ApprovalUnit.objects.filter(is_completed=False, user=request.user).order_by('-created')[:5]
    approvals = Approval.objects.filter(counsel__user=request.user)
    completed_appr = approvals.filter(is_completed=True).order_by('-created')[:5]
    proceed_appr = approvals.filter(is_completed=False).order_by('-created')[:5]
    return render(request, 'approval/index.html', {
        'approval_req': approval_req,
        'completed': completed_appr,
        'proceed': proceed_appr,
    })

def approval_detail_approve(request, pk):
    approval = Approval.objects.get(pk=pk)
    approvalUnit = ApprovalUnit.objects.get(approval_id=pk,user=request.user)

    if request.method == 'POST':
        btn = request.POST.get("btn")
        approvalUnit.is_completed = True
        approvalUnit.completed_date = datetime.datetime.now()
        if btn == 'approve':
            approvalUnit.is_approved = True

            count = approval.count
            if count == 1:
                approval.is_completed = True
                approval.is_approved = True
            elif count == 2:
                approval.count = 1
                ApprovalUnit.objects.create(
                    user = approval.n1,
                    approval = approval,
                )
            elif count == 3:
                approval.count = 2
                ApprovalUnit.objects.create(
                    user = approval.n2,
                    approval = approval,
                )
            elif count == 4:
                approval.count = 3
                ApprovalUnit.objects.create(
                    user = approval.n3,
                    approval = approval,
                )
            elif count == 5:
                approval.count = 4
                ApprovalUnit.objects.create(
                    user = approval.n4,
                    approval = approval,
                )
        elif btn == 'dismiss':
            approvalUnit.is_approved = False
            approval.is_completed = True
            approval.is_approved = False

        approval.save()
        approvalUnit.save()

        return HttpResponse('<script type="text/javascript">window.opener.location.reload();window.close();</script>')

    return render(request,'approval/approve_nav.html',{
        'approval': approval,
        'counsel': approval.counsel,
    })

def approval_detail_non_approve(request, pk):
    approval = Approval.objects.get(pk=pk)

    return render(request,'approval/non_approve_nav.html',{
        'approval': approval,
        'counsel': approval.counsel,
    })

def approval_req_list(request):
    approval_req = ApprovalUnit.objects.filter(is_completed=False, user=request.user).order_by('-created')
    return render(request, 'approval/list_req.html', {
        'approval_req': approval_req,
    })

def approval_completed_list(request):
    completed_appr = Approval.objects.filter(counsel__user=request.user, is_completed=True).order_by('-created')
    return render(request, 'approval/list_complete.html', {
        'completed_appr': completed_appr,
    })

def approval_proceed_list(request):
    proceed_appr = Approval.objects.filter(counsel__user=request.user, is_completed=False).order_by('-created')
    return render(request, 'approval/list_proceed.html', {
        'proceed_appr': proceed_appr,
    })

def approval_status(request, pk):
    approval = Approval.objects.get(pk=pk)
    try:
        n1 = ApprovalUnit.objects.get(approval=approval, user=approval.n1)
    except ApprovalUnit.DoesNotExist:
        n1 = None
    try:
        n2 = ApprovalUnit.objects.get(approval=approval, user=approval.n2)
    except ApprovalUnit.DoesNotExist:
        n2 = None
    try:
        n3 = ApprovalUnit.objects.get(approval=approval, user=approval.n3)
    except ApprovalUnit.DoesNotExist:
        n3 = None
    try:
        n4 = ApprovalUnit.objects.get(approval=approval, user=approval.n4)
    except ApprovalUnit.DoesNotExist:
        n4 = None
    try:
        n5 = ApprovalUnit.objects.get(approval=approval, user=approval.n5)
    except ApprovalUnit.DoesNotExist:
        n5 = None

    return render(request, 'approval/status.html', {
        'approval': approval, 'n1': n1, 'n2': n2, 'n3': n3, 'n4': n4, 'n5': n5,
    })

def approval_last_approved(request, pk):
    approval_list = ApprovalUnit.objects.filter(user=pk)
    return render(request, 'approval/last_approved.html', {
        'approval_list' : approval_list,
    })
