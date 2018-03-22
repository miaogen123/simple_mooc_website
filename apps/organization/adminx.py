# _*_ coding=utf-8 _*_

import  xadmin
from courses.models import Lesson



from .models  import CityDict, CourseOrg, Teacher



class TeacherInlines(object):
    model=Teacher
    extra=0


class CityDictAdmin(object):
    list_display=['name', 'desc','add_time']
    search_filed=['name', 'desc']
    list_filter=['name', 'desc','add_time']


class CourseOrgAdmin(object):
    list_display=['name','desc','click_nums','fav_nums','image','address','city','add_time']
    search_filed=['name','desc','click_nums','fav_nums','image','address','city']
    list_filter=['name','desc','click_nums','fav_nums','image','address','city','add_time']
    model_icon='fa fa-adn'
    ordering=['click_nums']
    readonly_fields=['fav_nums', 'click_nums']
    exclude=['image']
    relfield_style='fk_ajax'
    inlines=[TeacherInlines]



class TeacherAdmin(object):
    list_display=['org','name','work_years','work_company','points','click_nums', 'fav_nums','add_time', 'image']
    search_filed=['org','name','work_years','work_company','points','click_nums', 'fav_nums']
    list_filter=['org','name','work_years','work_company','points','click_nums', 'fav_nums','add_time','image']




xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
