
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic.base import  View
from django.http import  HttpResponse
from django.db.models import Q

from courses.models import Course, TeacherCourse, Video
from operation.models import UserCourse, UserFavorite, CourseComments
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def  get(self, request):
        all_courses=Course.objects.all()
        all_courses=all_courses.order_by('-add_time')
        hot_courses=all_courses.order_by('-click_nums')[:3]

        search_key=request.GET.get("keywords", '')
        if search_key:
            all_courses=Course.objects.filter(Q(name__icontains=search_key)|
                                              Q(desc__icontains=search_key)|
                                              Q(detail__icontains=search_key))

        sort=request.GET.get("sort", '')
        if sort=="hot":
            all_courses=all_courses.order_by('-click_nums')
        elif sort=='students':
            all_courses=all_courses.order_by('-students')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_courses,5,  request=request)

        courses= p.page(page)
        return render(request, "course-list.html", {
            "all_courses":courses,
            "hot_courses":hot_courses,
            "sort":sort,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course=Course.objects.get(id=course_id)
        chapter_nums=course.get_chapter()
        course.click_nums+=1
        course.save()
        students_learn=UserCourse.objects.filter(course=course_id)[:4]
        tag=course.tag
        if tag:
            rela_course=Course.objects.filter(Q(tag=tag)&~Q(id=course_id))[:1]
        else:
            rela_course=[]

        has_fav_org=False
        has_fav_course=False
        if request.user.is_authenticated():
            exist_records=UserFavorite.objects.filter(user=request.user, fav_id=(course_id), fav_type=1)
            if exist_records:
                has_fav_course=True
            exist_records=UserFavorite.objects.filter(user=request.user, fav_id=(course.course_org.id), fav_type=2)
            if exist_records:
                has_fav_org=True

        #teacher_nums=CourseOrg().get_teacher_num()
        #course=Course()
        #students=course.usercourse_set.all()[:5]

        return  render(request, "course-detail.html", {
            "chapter_nums":chapter_nums,
            "course":course,
            "students_learn": students_learn,
            "rela_course":rela_course,
            "has_fav_org":has_fav_org,
            "has_fav_course":has_fav_course,
        })

class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        if course_id == "":
            return
        course_s=Course.objects.get(id=int(course_id))
        #user_coursess=UserCourse.objects.filter(user=request.user, id=course_s.id)
        course_s.click_nums+=1
        course_s.save()
        user_coursess=UserCourse.objects.filter(user=request.user, course=course_s)
        if not user_coursess:
            user_course=UserCourse(user=request.user, course=course_s)
            user_course.save()
        user_courses=UserCourse.objects.filter(course=course_s)
        user_ids=[user_course.user.id for user_course in user_courses]
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        course_ids=[user_course.course.id  for user_course in user_courses]
        """
        获取相关的课程
        """
        relate_courses=Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:3]

        all_lessons=course_s.get_lessons()
        return render(request, "course-video.html",{
            "all_lessons":all_lessons,
            "course":course_s,
            "relate_courses":relate_courses,
            #"course_id":course_id,
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):

        if course_id == "":
            return
        course=Course.objects.get(id=int(course_id))
        user_courses=UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course=UserCourse(user=request.user, course=course_id)
            user_course.save()
        all_lessons=course.get_lessons()
        all_comments=course.get_comments()
        all_teacher=TeacherCourse.objects.filter(course_id=course_id)[:4]
        return render(request, "course-comment.html",{
            "all_lessons":all_lessons,
            "course":course,
            "all_teacher":all_teacher,
            "all_comments":all_comments,
            #"course_id":course_id,
        })


class AddCourseCommentView(View):
    """
    添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")
        comment=request.POST.get("comments", '')
        if  comment=="":
            return HttpResponse('{"status":"fail", "msg":"提交为空"}', content_type="application/json")
        courseid=request.POST.get("course_id",0)
        if int(courseid)>0 :
            course=Course.objects.get(id=int(courseid))
            if course:
                coursecomment=CourseComments()
                coursecomment.course_id=int(courseid)
                coursecomment.comments=comment
                coursecomment.user=request.user
                coursecomment.save()
                return HttpResponse('{"status":"success", "msg":"已提交"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"提交失败"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"提交失败"}', content_type="application/json")



class CoursePlayView(View):
    def get(self, request, video_id):
        if video_id== "":
            return
        video=Video.objects.get(id=int(video_id))
        #course_s = Course.objects.get(id=int(course_id))
        course_s=video.lesson.course
        course_s.students+=1
        course_s.save()
        """查询用户是否已经关联该课程"""
        user_coursess = UserCourse.objects.filter(user=request.user, id=course_s.id)
        if not user_coursess:
            user_course = UserCourse(user=request.user, course=course_s.id)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course_s)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in user_courses]
        """
        获取相关的课程
        """
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:3]

        all_lessons = course_s.get_lessons()
        return render(request, "course-play.html", {
            "all_lessons": all_lessons,
            "course": course_s,
            "relate_courses": relate_courses,
            "video":video,
            # "course_id":course_id,
        })
