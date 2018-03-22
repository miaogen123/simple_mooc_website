# _*_ coding=utf-8 _*_
__date__ = '3/9/2018 21:14 '
import  re

from django  import  forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    def clean_mobile(self):
        mobile=self.cleaned_data['mobile']
        MACTH_MOBILE="^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}"
        p=re.compile(MACTH_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号不匹配", code="mobile error")

    class Meta:
        model=UserAsk
        fields=['name','mobile','course_name']