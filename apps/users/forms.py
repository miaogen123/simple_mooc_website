
from django import forms
from django.forms import  ModelForm
from captcha.fields import CaptchaField
from captcha.models import CaptchaStore

from .models import UserProfile

class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True, min_length=5)


class  RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True, min_length=5)
    captcha=CaptchaField()


class  ForgetPwdForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha=CaptchaField()

class NewPwd(forms.Form):
    password=forms.CharField(min_length=8, required=True)
    password2=forms.CharField(min_length=8, required=True)
    email_to_modify=forms.EmailField(required=True)


class UploadImage(forms.ModelForm):

    class Meta:
        model=UserProfile
        fields=['image']

class UserInfo(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['nick_name', 'birthday' ,'gender', 'address' ,'mobile' ]
