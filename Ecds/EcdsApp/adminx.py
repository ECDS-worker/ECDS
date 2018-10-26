import xadmin
from xadmin import views

from .models import *


class UserInfoAdmin(object):
    list_display = ['name', 'age', 'gender', 'phone', 'email', 'address']
    search_fields = ['name', 'age', 'gender', 'phone', 'email', 'address']
    list_filter = ['name', 'age', 'gender', 'phone', 'email', 'address']


class CustormerAdmin(object):
    list_display = ['username', 'email', 'company', 'address', 'phone']
    search_fields = ['username', 'email', 'company', 'address', 'phone']
    list_filter = ['username', 'email', 'company', 'address', 'phone']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = "hhh后台管理系统"
    site_footer = "http://www.houhh.work"
    menu_style = "accordion"

xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(Custormer, CustormerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
