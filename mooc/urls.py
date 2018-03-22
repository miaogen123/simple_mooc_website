"""mooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve
from django.contrib import admin
from django.views.generic import TemplateView

from mooc.settings import MEDIA_ROOT
#STATIC_ROOT
from users.views import LoginView
from users.views import RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView, LogOutView
from organization.views import  WebIndexView
import  xadmin

#from users.views import  user_login

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',WebIndexView.as_view(), name="index" ),
    url(r'^login/$',LoginView.as_view(), name="login" ),
    url(r'^logout/$',LogOutView.as_view(), name="logout" ),
    url(r'^register/$',RegisterView.as_view(), name="register" ),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^resetpwd/(?P<active_code>.*)/$', ResetPwdView.as_view(), name="user_resetpwd"),
    #url(r'^resetpwd/(?P<active_code>.*)/$', ResetPwdView.as_view(), name="user_resetpwd"),
    url(r'^modify/$', ModifyPwdView.as_view(), name="modifypwd"),
    #url(r'^orglist/$', OrgList.as_view(), name="orglist"),

    url(r'^media/(?P<path>.*)$', serve , {"document_root":MEDIA_ROOT}),
    #url(r'^static/(?P<path>.*)$', serve , {"document_root":STATIC_ROOT}),

    url(r'^org/', include('organization.urls',namespace='org')),
    url(r'^courses/', include('courses.urls',namespace='courses')),
    url(r'^user/', include('users.urls',namespace='user')),

]

handler404="users.views.page_not_found"
handler500="users.views.page_error"
