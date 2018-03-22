from django.shortcuts import render
from django.db.models import  Q
from django.http import  HttpResponseRedirect
from django.views.generic.base import  View
from django.http import  HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import CourseOrg, CityDict
from .forms import UserAskForm
from courses.models import CourseOrg
from operation.models import UserFavorite
from .models import  Teacher
from courses.models import TeacherCourse, Course
from users.models import Banner



# Create your views here.


class OrgList(View):
    def get(self, request):
        all_orgs=CourseOrg.objects.all()
        all_dicts=CityDict.objects.all()

        catalog=request.GET.get('ct',"")
        city_id=request.GET.get('city', "")
        hot_orgs=CourseOrg.objects.order_by("-click_nums")[:3]
        sort=request.GET.get('sort',"")
        search_key=request.GET.get("keywords", '')
        if search_key:
            all_orgs=CourseOrg.objects.filter(Q(name__icontains=search_key)|
                                              Q(desc__icontains=search_key)|
                                              Q(address__icontains=search_key))

        if sort:
            if sort=="student":
                all_orgs=all_orgs.order_by("-student")
            elif sort=="course_nums":
                all_orgs=all_orgs.order_by("-course_nums")


        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))
        if catalog:
            all_orgs=all_orgs.filter(catalog=catalog)

        org_nums=all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs,5,  request=request)

        orgs= p.page(page)


        return render(request, "org-list.html",{
            "org_nums":org_nums,
            "all_orgs":orgs,
            "all_citys":all_dicts,
            "city_id":city_id,
            "catalog":catalog,
            "hot_orgs":hot_orgs,
            "sort":sort,
        })


class AddUserAskView(View):
    def post(self, request):
        userask=UserAskForm(request.POST)
        if userask.is_valid():
            user_ask=userask.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":u"提交出错"}' ,content_type="application/json")


class OrgHomeView(View):
    def get(self,request, org_id):
        current_page="home"
        course_org=CourseOrg.objects.get(id=int(org_id))
        all_courses=course_org.course_set.all()[:3]
        all_teachers=course_org.teacher_set.all()[:2]
        has_fav=False
        if request.user.is_authenticated():
             if UserFavorite.objects.filter( user=request.user,fav_id=course_org.id, fav_type=2):
                has_fav=True
            #if resu:
            #    resu=resu.filter()
            #    if resu:
            #        has_fav=True


        return render(request, 'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'current_page':current_page,
            'course_org':course_org,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    def get(self,request, org_id):
        current_page="course"
        course_org=CourseOrg.objects.get(id=int(org_id))
        all_courses=course_org.course_set.all()
        has_fav=False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter( user=request.user,fav_id=course_org.id, fav_type=2):
                has_fav=True
        return render(request, 'org-detail-course.html',{
            'all_courses':all_courses,
            'current_page':current_page,
            'course_org':course_org,
            'has_fav':has_fav,
        })


class OrgDescView(View):
    def get(self,request, org_id):
        current_page="desc"
        course_org=CourseOrg.objects.get(id=int(org_id))
        has_fav=False
        if request.user.is_authenticated():
            if  UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True
        return render(request, 'org-detail-desc.html',{
            'current_page':current_page,
            'course_org':course_org,
            'has_fav':has_fav,
        })


class OrgTeacher(View):
    def get(self,request, org_id):
        current_page="teacher"
        course_org=CourseOrg.objects.get(id=int(org_id))
        has_fav=False
        if request.user.is_authenticated():
            if  UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True
        all_teachers=course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',{
            'current_page':current_page,
            'course_org':course_org,
            'all_tearchers':all_teachers,
            'has_fav':has_fav,
        })


class AddFavView(View):
    def post(self,request):
        fav_id=request.POST.get('fav_id', 0)
        fav_type=request.POST.get('fav_type', 0)
        has_fav=False
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        exist_records=UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        #exist_records=UserFavorite.objects.filter(user=request, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
            if int(fav_type)==1:
                course=Course.objects.get(id=int(fav_id))
                if course.fav_nums<=0:
                    course.fav_nums=0
                else:
                    course.fav_nums-=1
                    course.save()
                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
            elif int(fav_type)==2:
                courseorg = CourseOrg.objects.get(id=int(fav_id))
                if courseorg.fav_nums <= 0:
                    courseorg.fav_nums = 0
                else:
                    courseorg.fav_nums -= 1
                    courseorg.save()
                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
            elif int(fav_type) == 3:
                teacher= Teacher.objects.get(id=int(fav_id))
                if teacher.fav_nums <= 0:
                    teacher.fav_nums = 0
                else:
                    teacher.fav_nums -= 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav=UserFavorite()
            if int(fav_id)>0  and int(fav_type)>0 :
                user_fav.user=request.user
                user_fav.fav_type=int(fav_type)
                user_fav.fav_id=int(fav_id)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                    return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
                elif int(fav_type) == 2:
                    courseorg= CourseOrg.objects.get(id=int(fav_id))
                    courseorg.fav_nums += 1
                    courseorg.save()
                    return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
                elif int(fav_type) == 3:
                    teacher= Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                    return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    def get(self,request):
        all_teachers=Teacher.objects.all()
        sort=request.GET.get("sort", '')
        teacher_nums=all_teachers.count()
        hot_teachers=all_teachers.order_by('-fav_nums')[:3]
        search_key=request.GET.get("keywords", '')
        if search_key:
            all_teachers=Teacher.objects.filter(Q(name__icontains=search_key)|
                                              Q(desc__icontains=search_key)|
                                              Q(work_company__icontains=search_key))
        if sort:
            if sort =="hot":
               all_teachers=all_teachers.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers ,2,  request=request)

        all_teachers= p.page(page)
        return render(request, "teachers-list.html", {
            "all_teachers":all_teachers,
            "teacher_nums":teacher_nums,
            "sort":sort,
            "hot_teachers":hot_teachers,
        })


class TeacherDetailView(View):
    def get(self,request, teacher_id):

        if teacher_id=="":
            return HttpResponseRedirect('/org/teacher/list/')
        teacher_id=int(teacher_id)
        teacher=Teacher.objects.get(id=teacher_id)
        teacher.click_nums+=1
        teacher.save()
        teachercouses=TeacherCourse.objects.filter(teacher_id=teacher_id)
        course_ids=[course_id.course_id for course_id in teachercouses]
        all_courses=Course.objects.filter(id__in=course_ids)
        hotteachers=Teacher.objects.all().order_by('-fav_nums')[:3]

        has_fav_org=False
        has_fav_teacher=False
        if request.user.is_authenticated():
            exist_records=UserFavorite.objects.filter(user=request.user, fav_id=(teacher_id), fav_type=3)
            if exist_records:
                has_fav_teacher=True
            exist_records=UserFavorite.objects.filter(user=request.user, fav_id=(teacher.org.id), fav_type=2)
            if exist_records:
                has_fav_org=True

        return render(request, "teacher-detail.html", {
            "teacher":teacher,
            "all_courses":all_courses,
            "hotteachers":hotteachers,
            "has_fav_org":has_fav_org,
            "has_fav_teacher":has_fav_teacher,
        })


class WebIndexView(View):
    def get(self,request):
        allbanners=Banner.objects.all()[:5]
        banner_courses=Course.objects.filter(is_banner=True)[:3]
        courses=Course.objects.filter(is_banner=False)[:6]
        orgs=CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "allbanners":allbanners,
            "banner_courses":banner_courses,
            "courses":courses,
            "orgs":orgs,
        })
