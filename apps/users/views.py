# _*_ coding=utf-8 _*_
import  json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import  logout
from django.core.urlresolvers import reverse

from django.db.models import  Q
from django.views.generic.base import  View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from users.models import UserProfile
from .forms import LoginForm, RegisterForm, ForgetPwdForm, NewPwd, UploadImage, UserInfo
from utils.email_send  import  send_register_email
from users.models import EmailVerify
from  utils.mixin_utils import LoginRequiredMixin
from  courses.models import  Course, Teacher
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import CourseOrg
# Create your views here.





class CustomBackends(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records=EmailVerify.objects.filter(code=active_code)
        if all_records:
            user_id=0
            for records in all_records:
                email=records.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user_id=user.id
                user.save()
            add_message=UserMessage()
            add_message.message="欢迎来到mooc网，请享受一次完整的大保健,xixixi~"
            add_message.user=user_id
            add_message.user_from=1
            add_message.save()


        else:
            return render(request, "active_fail.html")


class RegisterView(View):
    def get(self, request):
        registerform=RegisterForm()
        return render(request, "register.html", {'registerform':registerform})
    def post(self, request):
        registerform=RegisterForm()
        #print (formset.errors)

        #TODO:: the logical here is wrong: search the duplication first

        #if registerform.is_valid():
        user_name=request.POST.get("email", "")
        if UserProfile.objects.filter(email=user_name):
            return render(request, "register.html",{ "registerform":registerform, "msg":"用户已存在"})
        pass_word=request.POST.get("password", "")
        user_profile=UserProfile()
        user_profile.username=user_name
        user_profile.email=user_name
        user_profile.is_active=False

        user_profile.password =make_password(pass_word)

        user_profile.save()

        send_register_email(user_profile.email, "register" )

        return render(request, "register.html",{ "msg":"已发送验证链接，请注意查收" })
        #pass


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            pass
        user_name=request.POST.get("username", "")
        pass_word=request.POST.get("password", "")
        userpassword=make_password("qsc12345")
        user=authenticate(username=user_name, password=pass_word)

        #userpassword=make_password("admin123")
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html",{ "msg":"用户未激活", "login_form":login_form })
        else:
            return render(request, "login.html",{ "msg":"用户名或密码错误", "login_form":login_form })


class LogOutView(View):
    """
    用户登出的逻辑
    """
    def get(self,request):
        if request.user:
            logout(request)
            return HttpResponseRedirect(reverse("index"))



class ForgetPwdView(View):
    def get(self, request):
        forgetpwdform=ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwdform":forgetpwdform})
    def post(self, request):
        forgetpwdform=ForgetPwdForm(request.POST)
        if forgetpwdform.is_valid():
            email=request.POST.get("email", "")
            result=UserProfile.objects.filter(email=email)
            if result:
                send_register_email(email,"forget")
            return render(request, 'forgetpwd.html', {"msg":"请单击您邮箱里的链接完成验证"})
        else:
            return render(request, "forgetpwd.html", {"msg":"提交错误，请重新输入"})


class ResetPwdView(View):

    def get(self, request, active_code):
        records=EmailVerify.objects.filter(code=active_code)
        if records :
            for record in records:
                email=record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "reset_error.html")


class  ModifyPwdView(View):
    def post(self, request):
        if True:
            newpwdform=NewPwd(request.POST)
        #if newpwdform.is_valid():
            passwd1=request.POST.get("password", "")
            passwd2=request.POST.get("password2", "")
            if passwd1!=passwd2:
                #TODO:: need more security work
                return render(request, "reset_error.html")
            else:
                email=request.POST.get("email","")
                #check_reseult=EmailVerify.objects.filter(email=email, code=)
                user=UserProfile.objects.get(email=email)
                user.password=make_password(passwd2)
                user.save()
                return render(request, "index.html")
        else:
            return render(request, "reset_error.html")


class UserInfoView( LoginRequiredMixin, View):
    def get(self, request):
        currentpage="info"
        return render(request, "usercenter-info.html", {
            "currentpage":currentpage,
        })

    def post(self,request):
        userinfoch=UserInfo(request.POST,  instance=request.user)
        if userinfoch.is_valid():
            userinfoch.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(UserInfo.errors), content_type="application/json")




class UserCourseView(LoginRequiredMixin, View):
    def get(self, request):
        currentpage="course"
        user=request.user
        uesr_cousers=UserCourse.objects.filter(user_id=user.id)
        course_ids=[course.course_id for course in uesr_cousers]
        courses=Course.objects.filter(id__in=course_ids)
        #course_org_fav=UserFavorite.objects.filter(org_id=course.course_org.id, )
        return  render(request, "usercenter-mycourse.html", {
            "currentpage":currentpage,
            "courses":courses,
        })



class UserFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        currentpage="userfavcourses"
        user=request.user
        user_fav_courses=UserFavorite.objects.filter(user=user, fav_type=1)
        course_ids=[user_fav.fav_id for user_fav in user_fav_courses]
        courses=Course.objects.filter(id__in=course_ids)
        return  render(request, "usercenter-fav-course.html", {
            "currentpage":currentpage,
            "courses":courses,
        })


class UserFavOrgsView(LoginRequiredMixin, View):
    def get(self, request):
        currentpage="userfavorgs"
        user=request.user
        user_fav_courses=UserFavorite.objects.filter(user=user, fav_type=2)
        org_id=[user_fav.fav_id for user_fav in user_fav_courses]
        orgs=CourseOrg.objects.filter(id__in=org_id)
        return  render(request, "usercenter-fav-org.html", {
            "currentpage":currentpage,
            "orgs":orgs,
        })


class UserFavTeachersView(LoginRequiredMixin, View):
    def get(self, request):
        currentpage="userfavteachers"
        user=request.user
        user_fav_courses=UserFavorite.objects.filter(user=user, fav_type=3)
        teacher_id=[user_fav.fav_id for user_fav in user_fav_courses]
        teachers=Teacher.objects.filter(id__in=teacher_id)

        return  render(request, "usercenter-fav-teacher.html", {
            "currentpage":currentpage,
            "teachers":teachers,
        })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        currentpage="message"
        user=request.user
        UserProfile(user).ReleaseMessage()
        user_messages=UserMessage.objects.filter(user=user.id)
        #course_org_fav=UserFavorite.objects        try:
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(user_messages,2,  request=request)
        user_messages= p.page(page)
        return  render(request, "usercenter-message.html", {
            "currentpage":currentpage,
            "user_messages":user_messages,
        })


class UploadImageView(LoginRequiredMixin, View):
    """
    修改用户头像
    """
    def post(self, request):
        """
        modelform  既有model的属性又有form 的属性，但感觉默认的是form 的属性，加上一个instance以后相当于对之中model部分进行了实例化
        """
        uploadimage=UploadImage(request.POST, request.FILES, instance=request.user)
        if uploadimage.is_valid():
            uploadimage.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json")


class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form=NewPwd(request.POST)
        if modify_form.is_valid():
            password1=request.POST.get("password1", '')
            password2=request.POST.get("password2", '')
            if not (password1== password2):
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type="application/json")
            else:
                user=request.user
                user.password=make_password(password1)
                user.save()
                return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email=request.GET.get("email", '')
        if email:
            exist=UserProfile.objects.filter(email=email)
            if exist:
                return HttpResponse('{"email":"邮箱已经存在"}', content_type="application/json")
            else:
                send_register_email(email, "update")
                return HttpResponse('{"email":"邮件已发送"}', content_type="application/json")
        else:
            return HttpResponse('{"email":"邮箱不能为空"}', content_type="application/json")


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email=request.POST.get("email", '')
        code=request.POST.get("code", '')
        exist_record=EmailVerify.objects.filter(email=email, code=code, send_type="update")
        if exist_record:
            user=request.user
            user.email=email
            user.save()
            return HttpResponse('{"email":"修改成功"}', content_type="application/json")
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type="application/json")


def page_not_found(request):
    from django.shortcuts import render_to_response
    response =render_to_response('404.html', {})
    response.status_code=404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response =render_to_response('500.html', {})
    response.status_code=500
    return response
