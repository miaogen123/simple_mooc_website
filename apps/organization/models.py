# _*_ coding=utf-8 _*_
from datetime import  datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name=models.CharField(max_length=20, verbose_name=u"城市")
    desc=models.TextField(verbose_name=u"城市描述")
    add_time=models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name="城市"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name=models.CharField(max_length=50, verbose_name=u"机构名称")
    desc=models.TextField(verbose_name=u"机构描述")
    catalog=models.CharField(default='pxjg', max_length=20, verbose_name=u"所属机构", choices=(('pxjg', u"培训机构"),('gr', u'个人'),('gx', '高校') ))
    click_nums=models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums=models.IntegerField(default=0, verbose_name=u"收藏数")
    image=models.ImageField(upload_to="org/%Y/%m", verbose_name=u"封面图片")
    address=models.CharField(max_length=50, verbose_name=u"机构地址")
    city=models.ForeignKey(CityDict,  verbose_name=u"城市")
    student=models.IntegerField(default=0, verbose_name=u"学习人数")
    course_nums=models.IntegerField(default=0, verbose_name=u"课程数")
    org_tag=models.CharField(default="全国知名", verbose_name=u"课程标签", max_length=8)
    add_time=models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name="机构信息"
        verbose_name_plural=verbose_name

    def get_teacher_num(self):
        return self.teacher_set.all().count()

    #the two lines code below makes the name showed in the select box
    def __str__(self):
        return self.name


class Teacher(models.Model):
    org=models.ForeignKey(CourseOrg, verbose_name=u"所属机构")
    name=models.CharField(max_length=50, verbose_name=u"教师名称")
    work_years=models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company=models.CharField(max_length=100, verbose_name=u"公司")
    work_job=models.CharField(max_length=10, verbose_name=u"职位", default="讲师")
    age=models.IntegerField( verbose_name=u"年龄", default=0)
    image=models.ImageField(upload_to="tearcher/%Y/%m", verbose_name=u"头像", default="teacher/2018/03/default.png")
    points=models.TextField(verbose_name=u"授课特点")
    click_nums=models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums=models.IntegerField(default=0, verbose_name=u"收藏数")
    add_time=models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name="教师信息"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name



