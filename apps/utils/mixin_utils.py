# _*_ coding=utf-8 _*_
__date__ = '3/14/2018 20:44 '

from django.contrib.auth.decorators import login_required
from django.utils.decorators import  method_decorator

class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)