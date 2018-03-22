# _*_ coding=utf-8 _*_
__date__ = '3/5/2018 21:33 '

from random import  Random

from django.core.mail import  send_mail


from users.models import EmailVerify
from mooc.settings import EMAIL_FROM


def random_str(randomlength=0):
    str=''
    chars ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length=len(chars) -1
    random=Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def send_register_email(email, send_type="register"):
    email_record=EmailVerify()
    if send_type=="update":
        code=random_str(4)
    else:
        code=random_str(16)
    email_record.code=code
    print ("")
    print (code)
    print ("")
    email_record.email=email
    email_record.send_type=send_type
    email_record.save()

    email_title=""
    email_body=""

    if send_type=="register":
        email_title="慕学在线"
        email_body="click  the link http:\\localhost:8000\\active\\{0}   to active you account".format(code)

        send_status=send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type=="forget":
        email_title="慕学在线"
        email_body="click  the link http:\\localhost:8000\\resetpwd\\{0} to recover your password ".format(code)

        send_status=send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type=="update":
        email_title="慕学在线"
        email_body="click  the link http:\\localhost:8000\\resetpwd\\{0} to update your password ".format(code)

        send_status=send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

