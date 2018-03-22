# _*_ coding=utf-8 _*_
__date__ = '3/9/2018 21:17 '

from django.conf.urls import  url, include

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCourseCommentView, CoursePlayView


urlpatterns=[
    url(r'^list/$', CourseListView.as_view(), name='list'),
    url(r'^details/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="details"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="info"),
    #url(r'^comment/$', CourseCommentView.as_view(), name="comment"),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="comment"),
    url(r'^addcomment/$', AddCourseCommentView.as_view(), name="addcomment"),
    url(r'^video/(?P<video_id>\d+)/$', CoursePlayView.as_view(), name="video"),

]
