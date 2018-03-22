# _*_ coding=utf-8 _*_
from datetime import  datetime

from django.db import models

from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org=models.ForeignKey(CourseOrg,verbose_name=u"课程机构", null=True, blank=True)
    name=models.CharField(max_length=50, verbose_name=u"课程名")
    desc=models.CharField(max_length=50, verbose_name=u"课程描述")
    detail=models.TextField(verbose_name=u"课程细节")
    degree=models.CharField(choices=(('hard', u'难'),('middle', u'普通'), ('easy', '简单')),max_length=6)
    learn_times=models.IntegerField(default=0, verbose_name=u"学习时长")
    students=models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums=models.IntegerField(default=0, verbose_name=u"收藏人数")
    image=models.ImageField(upload_to="Courses/%Y/%m", verbose_name="封面图片")
    click_nums=models.IntegerField(default=0, verbose_name=u"点击人数")
    add_time=models.DateTimeField(default=datetime.now)
    category=models.CharField(max_length=20, default=u"后端", verbose_name=u"类别")
    tag=models.CharField(max_length=10, default='', verbose_name=u"标签")
    is_banner=models.BooleanField(default=False, verbose_name=u"是否是轮播图")
    course_tag=models.CharField(max_length=8, verbose_name=u"课程标签", default="全国知名")
    #to be used
    price=models.IntegerField(verbose_name=u"课程价格")

    def get_comments(self):
        return self.coursecomments_set.all()

    def get_chapter(self):
        return self.lesson_set.all().count()
    get_chapter.short_description=u"章节数"

    def get_lessons(self):
        return self.lesson_set.all()

    def get_students(self, course_id):
        return  self.usercourse_set.all()[:5]
    #    return students

    class Meta:
            verbose_name=u"课程名"
            verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name=u"轮播课程"
        verbose_name_plural=verbose_name
        proxy=True
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='www.baidu.com'>百度</a>")
    go_to.short_description = u"链接"


class Lesson(models.Model):
    course=models.ForeignKey(Course, verbose_name=u"课程")
    name=models.CharField(max_length=50, verbose_name=u"章节名")
    add_time=models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name=u"章节名"
        verbose_name_plural=verbose_name

    def get_video(self):
        return self.video_set.all()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson=models.ForeignKey(Lesson, verbose_name=u"章节")
    name=models.CharField(max_length=100, verbose_name=u"视频名")
    video_url=models.CharField(max_length=200, verbose_name=u"视频链接", default='')
    time=models.CharField(max_length=6, default='', verbose_name=u"视频时长")
    add_time=models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name=u"视频名"
        verbose_name_plural=verbose_name
    def get_resourse(self):
           return self.video_set.all()
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name


class CourseResource(models.Model):
    video=models.ForeignKey(Video, verbose_name=u"视频")
    name=models.CharField(max_length=100, verbose_name=u"资料名")
    download=models.FileField(upload_to="courses/resource/%Y/%m", verbose_name=u"下载" ,max_length=100)
    add_time=models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name=u"资料"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class TeacherCourse(models.Model):
    teacher=models.ForeignKey(Teacher, verbose_name=u"课程教师")
    course=models.ForeignKey(Course, verbose_name=u"课程")
    need_know_before=models.CharField(max_length=200, default='' , verbose_name=u"课程须知")
    to_tell_you=models.CharField(max_length=200, default='' , verbose_name=u"老师告诉你")

    class Meta:
        verbose_name=u"教师课程"
        verbose_name_plural=verbose_name

    def __str__(self):
        #return self.Meta.verbose_name
        return u"教师课程"
