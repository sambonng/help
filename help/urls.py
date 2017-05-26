"""help URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/update/$', views.update_profile, name='profile-update'),
    url(r'^profile/change-password/$', views.change_password, name='profile-change-password'),
    url(r'^signup/$', views.signup, name='signup'),

    url(r'^announcement/$', views.announcement_list, name='announcement-list'),
    url(r'^announcement/create/$', views.announcement_create, name='announcement-create'),
    url(r'^announcement/(?P<pk>\d+)/$', views.announcement_detail, name='announcement-detail'),
    url(r'^announcement/(?P<pk>\d+)/update/$', views.announcement_update, name='announcement-update'),
    url(r'^announcement/(?P<pk>\d+)/delete/$', views.announcement_delete, name='announcement-delete'),

    url(r'^soldier/$', views.soldier_list, name='soldier-list'),
    url(r'^soldier/create/$', views.soldier_create, name='soldier-create'),
    url(r'^soldier/(?P<pk>\d+)/$', views.soldier_detail, name='soldier-detail'),
    url(r'^soldier/(?P<pk>\d+)/enroll/$', views.soldier_enroll_user, name='soldier-enroll-user'),
    url(r'^soldier/(?P<pk>\d+)/update/$', views.soldier_update, name='soldier-update'),

    url(r'^counsel/$', views.counsel, name='counsel'),
    url(r'^counsel/(?P<pk>\d+)/$', views.counsel_list, name='counsel-list'),
    url(r'^counsel/(?P<pk>\d+)/create/$', views.counsel_create, name='counsel-create'),
    url(r'^counsel/(?P<pk>\d+)/(?P<pkc>\d+)/$', views.counsel_detail, name='counsel-detail'),
    url(r'^counsel/(?P<pk>\d+)/create/popup/$', views.counsel_create_popup, name='counsel-create-popup'),

    url(r'^approval/$', views.approval, name='approval'),
    url(r'^approval/(?P<pk>\d+)/approve/$', views.approval_detail_approve, name='approval-detail-approve'),
    url(r'^approval/(?P<pk>\d+)/$', views.approval_detail_non_approve, name='approval-detail-non-approve'),
    url(r'^approval/(?P<pk>\d+)/status/$', views.approval_status, name='approval-status'),
    url(r'^approval/requestlist/$', views.approval_req_list, name='approval_req_list'),
    url(r'^approval/completedlist/$', views.approval_completed_list, name='approval_completed_list'),
    url(r'^approval/proceedlist/$', views.approval_proceed_list, name='approval_proceed_list'),
    url(r'^approval/(?P<pk>\d+)/approved-list', views.approval_last_approved, name='approval-last-approved'),

    url(r'^ajax/counsel_find_user/(?P<pk>\d+)/$', views.ajax_counsel, name='find-userlist'),
    url(r'^ajax/soldier_find_user/(?P<pk>\d+)/$', views.ajax_soldier, name='user-search'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
