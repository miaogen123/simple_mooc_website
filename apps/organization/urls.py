# _*_ coding=utf-8 _*_
__date__ = '3/9/2018 21:17 '

from django.conf.urls import  url, include

from .forms import UserAskForm
from .views import OrgList, AddUserAskView, TeacherListView
from organization.views import OrgHomeView, OrgCourseView, OrgDescView, OrgTeacher, AddFavView, TeacherDetailView


urlpatterns=[
    url(r'^list/$', OrgList.as_view(), name='org_userask'),
    url(r'^add_userask/', AddUserAskView.as_view(), name='add_userask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^orgcourse/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^orgdesc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^orgteacher/(?P<org_id>\d+)/$', OrgTeacher.as_view(), name="org_teacher"),
    url(r'^add_fav/', AddFavView.as_view(), name='add_fav'),
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),

]