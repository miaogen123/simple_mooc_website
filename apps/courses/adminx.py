# _*_ coding=utf-8 _*_

import  xadmin

from .models  import Course, Lesson, Video, CourseResource, TeacherCourse
from courses.models import BannerCourse

class CourseAdmin(object):
    list_display=['name', 'desc','detail', 'degree', 'learn_times','students']
    search_filed=['name', 'desc','detail', 'degree', 'students']
    list_filter=['name', 'desc','detail', 'degree', 'learn_times','students']


class LessonAdmin(object):
    list_display=['name','course','add_time']
    search_filed=['name','course']
    list_filter=['name','course__name','add_time']


class VideoAdmin(object):
    list_display=['lesson','name','add_time']
    search_filed=['lesson','name']
    list_filter=['lesson','name','add_time']


class CourseResourceAdmin(object):
    list_display=['video','name','download','add_time']
    search_filed=['video','name','download']
    list_filter= ['video','name','download','add_time']


class TeacherCourseAdmin(object):
    list_display=['teacher','course','need_know_before','to_tell_you']
    search_filed=['teacher','course','need_know_before','to_tell_you']
    list_filter= ['teacher','course','need_know_before','to_tell_you']


class BannerCourseAdmin(object):
    list_display=['name', 'desc','detail' , 'get_chapter', 'go_to']
    search_filed=['name', 'desc']
    list_filter=['name', 'desc','detail']

    def queryset(self):
        qs=super(BannerCourseAdmin, self).queryset()
        qs=qs.filter(is_banner=True)
        return qs

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(TeacherCourse, TeacherCourseAdmin)
