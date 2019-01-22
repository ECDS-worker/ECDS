from api.utils import *


# 登陆用户必须为票交所发布管理员
def ecdsuser_release(func):
    def _wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return permission_denied()
        permission_code = request.session.get('permission_code')
        if permission_code != 3:
            return permission_denied()
        return func(self, request, *args, **kwargs)
    return _wrapper


# 登陆用户必须为票交所 应用 管理员
def ecdsuser_application(func):
    def _wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return permission_denied()
        permission_code = request.session.get('permission_code')
        if permission_code != 4:
            return permission_denied()
        return func(self, request, *args, **kwargs)
    return _wrapper


# 登陆用户必须为票交所 应用录入 管理员
def ecdsuser_input(func):
    def _wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return permission_denied()
        permission_code = request.session.get('permission_code')
        if permission_code != 5:
            return permission_denied()
        return func(self, request, *args, **kwargs)
    return _wrapper


# 登录用户必须为测试用户
def commentuser_required(func):
    def _wrapper(self, request, *args, **kwargs):
        if not request.session.get("username"):
            return permission_denied()
        permission_code = request.session.get('permission_code')
        if permission_code not in [1, 2]:
            return permission_denied()
        return func(self, request, *args, **kwargs)
    return _wrapper
