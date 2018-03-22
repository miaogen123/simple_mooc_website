import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from .models import EmailVerify,Banner
from users.models import UserProfile


class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True


class GlobalSetting(object):
    site_title="MOOC后台"
    site_footer="MOOC网"
    menu_style="accordion"

class EmailVerifyAdmin(object):
    list_display=['email', 'code', 'send_type', 'sent_time']
    search_fields=['email', 'code', 'send_type']
    list_filter=['email', 'code', 'send_type', 'sent_time']


class BannerAdmin(object):
    list_display=['title', 'image', 'url', 'index', 'add_time']
    search_fields=['email', 'code', 'send_type', 'index']
    list_filter=['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerify, EmailVerifyAdmin)

xadmin.site.register(Banner, BannerAdmin)

#xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
