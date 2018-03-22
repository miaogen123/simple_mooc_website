# _*_ coding=utf-8 _*_
from  __future__  import unicode_literals
from datetime import  datetime

from django.db import models
from django.contrib.auth.models import  AbstractUser



# Create your models here.


class UserProfile(AbstractUser):
    nick_name=models.CharField(max_length=50, verbose_name=u"昵称")
    birthday=models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender=models.CharField(max_length=11, choices=(('male', u"男"), ('female', u"女")), default='female')
    address=models.CharField(max_length=100, default="", null=True)
    mobile=models.CharField(max_length=11, null=True, blank=True)
    image=models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name="用户信息"
        verbose_name_plural=verbose_name

    def NewMessage(self):
        from operation.models import UserMessage
        count=UserMessage.objects.filter(user=self.id, has_read=0).count()
        print("test")
        return count

    def ReleaseMessage(self):
        from operation.models import UserMessage
        user_messages=UserMessage.objects.filter(user=self.id, has_read=0)
        for message in user_messages:
            message.has_read=1
            message.save()
        return
    def __unicode__(self):
        return self.username

class  EmailVerify(models.Model):
    email=models.EmailField(max_length=50, verbose_name=u"邮箱")
    code=models.CharField(max_length=16, verbose_name=u"验证码")
    send_type=models.CharField(max_length=10, choices=(('regester', u"注册"), ('forget', u"忘记密码")))
    sent_time=models.TimeField(default=datetime.now)

    class Meta:
        verbose_name=u"验证码"
        verbose_name_plural=verbose_name

class Banner(models.Model):
    title=models.CharField(max_length=20, verbose_name=u"标题")
    image=models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图")
    url=models.URLField(max_length=200, verbose_name=u"访问地址")
    index=models.IntegerField(default=100, verbose_name=u"顺序")
    add_time=models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"轮播图"
        verbose_name_plural=verbose_name



