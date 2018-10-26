import random
import base64

from api.comment import Rest
from django.contrib.auth import authenticate, logout, login
from api.utils import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class SessionRest(Rest):
    def post(self, request, *args, **kwargs):
        data = request.POST

        username = data.get('username', '')
        password = data.get('password', '')
        username = str(base64.b64decode(username), encoding='utf-8')[8:]
        password = str(base64.b64decode(password), encoding="utf-8")[8:]
        permission_code = data.get('permission_code', '0')
        request.session["permission_code"] = permission_code

        retu_data = {
            "msg": '',
            "permission_code": ''
        }

        # 查询数据库用户表
        user = authenticate(username=username, password=password)
        if user:
            if (permission_code in ('1', '2')) and hasattr(user, 'userinfo'):
                # 保存登陆状态
                login(request, user)
                retu_data["msg"] = "登陆成功"
                retu_data["status"] = "200"
                retu_data["permission_code"] = permission_code
            elif (permission_code == '3') and hasattr(user, 'custormer'):
                # 保存登陆状态
                login(request, user)
                retu_data["msg"] = "登陆成功"
                retu_data["status"] = "200"
                retu_data["permission_code"] = permission_code

            else:
                retu_data["msg"] = "没有登陆权限"
                retu_data["status"] = "403"

        else:
            retu_data["msg"] = "用户名或密码错误"
            retu_data["status"] = "403"

        return json_response(retu_data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return json_response({
          "msg": "退出成功"
        })


class UserRest(Rest):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            # 获取信息
            data = dict()
            # 有坑，定义表时，表名为custormer 正确的是customer，涉及到此表的都要注意
            if hasattr(user, 'custormer'):
                custome = user.custormer
                data['username'] = custome.username
                data['email'] = custome.email
                data['user'] = user.id
                data['category'] = 'customer'
            elif hasattr(user, 'userinfo'):
                userinfo = user.userinfo
                data['username'] = userinfo.username
                data['qq'] = userinfo.qq
                data['user'] = user.id
                data['category'] = 'userinfo'
            else:
                return json_response({})
        else:
            return not_authenbticated()
        return json_response(data)

    def post(self, request, *args, **kwargs):
        # 创建用户
        data = request.POST
        username = data.get('username', '')
        password = data.get('password', '')
        ensure_password = data.get('ensure_password', '')
        regist_code = data.get('regist_code', 0)
        session_regist_code = request.session.get('regist_code', 1)

        error = dict()
        if not username:
            error['username'] = '必须提供用户名'
        else:
            if User.objects.filter(username=username).count() > 0:
                error['username'] = '用户名已存在'
        if len(password) < 6:
            error['password'] = '密码长度不可小于6位'
        if password != ensure_password:
            error['ensure_password'] = '密码不匹配'
        if regist_code != session_regist_code:
            error['regist_code'] = '验证码不匹配'
        if error:
            return params_error(error)
        user = User()
        user.username = username
        user.set_password(password)
        user.save()
        return json_response({'id': user.id})


class RegistCode(Rest):
    def get(self, request, *args, **kwargs):
        # 获取随机验证码
        regist_code = random.randint(100000, 1000000)
        # 保存到session中
        request.session['regist_code'] = regist_code
        # 返回随机数
        return json_response({
            'regist_code': regist_code
        })
