# _*_ coding=utf-8 _*_
__date__ = '3/15/2018 20:41 '

from django.conf.urls import  url, include

from .views import UserInfoView, UserCourseView, UserFavCourseView, UserFavOrgsView, UserFavTeachersView, UserMessageView, UploadImageView, UpdatePwdView, SendEmailCodeView
from .views import UpdateEmailView


urlpatterns=[
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^courses/$', UserCourseView.as_view(), name='user_courses'),
    url(r'^favcourses/$', UserFavCourseView.as_view(), name='favcourses'),
    url(r'^favorgs/$', UserFavOrgsView.as_view(), name='favorgs'),
    url(r'^favteachers/$', UserFavTeachersView.as_view(), name='favteachers'),
    url(r'^messages/$', UserMessageView.as_view(), name='messages'),
    url(r'^uploadimage/$', UploadImageView.as_view(), name='uploadimage'),
    url(r'^updatepwd/$', UpdatePwdView.as_view(), name='updatepwd'),
    url(r'^sendcode/$', SendEmailCodeView.as_view(), name='sendcode'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),



]
