import random
import datetime

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from api.utils import *
from api.comment import Rest
from EcdsApp.models import Commentuser

User = get_user_model()


class Login(Rest):
    """
        用户登陆
    """
    count = 0

    def post(self, request, *args, **kwargs):
        data = request.POST

        username = data.get('username', '')
        password = data.get('password', '')
        # username = str(base64.b64decode(username), encoding='utf-8')[8:]
        # password = str(base64.b64decode(password), encoding="utf-8")[8:]
        regist_code = data.get('regist_code', '')
        retu_data = {
            "msg": "",
            "permission_code": "",
        }
        if request.session.get('regist_code') != regist_code:
            retu_data["msg"] = "验证码错误"
        else:

            # 查询数据库用户表
            user = authenticate(username=username, password=password)
            if user:
                # 保存登陆状态
                login(request, user)
                permission_code = user.role
                retu_data["msg"] = "登陆成功"
                retu_data["status"] = "200"
                retu_data["permission_code"] = permission_code
                request.session["permission_code"] = permission_code
            elif Commentuser.objects.get(username=username, user_pw=password):
                request.session["username"] = username
                permission_code = Commentuser.objects.get(username=username).role
                # 保存登陆状态
                retu_data["msg"] = "登陆成功"
                retu_data["status"] = "200"
                retu_data["permission_code"] = permission_code
                request.session["permission_code"] = permission_code
            else:
                try:
                    if request.session["logincount"] == 0:
                        self.count = 0
                except:
                    pass
                self.count += 1
                request.session["logincount"] = 1
                if self.count >= 5:
                    retu_data["logincount"] = 5
                    request.session["logincount"] = 5
                    time_session = datetime.datetime.now() + datetime.timedelta(minutes=1)
                    request.session["nowtime"] = time_session.strftime("%M")
                    if datetime.datetime.now().strftime("%M") >= request.session["nowtime"]:
                        self.count = 0
                        request.session["logincount"] = 0
                retu_data["msg"] = "用户名或密码错误"
                retu_data["status"] = "403"

        request.session['regist_code'] = "!@#$%^&*()"
        return json_response(retu_data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        request.session.clear()
        return json_response({
          "msg": "退出成功"
        })


class RegistUser(Rest):
    """
        创建用户
    """
    def post(self, request, *args, **kwargs):
        pass


class UserRest(Rest):
    """
        用户信息展示
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            # 获取信息
            data = dict()

            if hasattr(user, 'Commentuser'):
                custome = user.Commentuser
                data['username'] = custome.username
                data['email'] = custome.email
                data['user'] = user.id
            elif hasattr(user, 'EcdsUser'):
                userinfo = user.userinfo
                data['username'] = userinfo.username
                data['qq'] = userinfo.qq
                data['user'] = user.id
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
    """
        登陆验证码
    """
    logincount = 0

    def get(self, request, *args, **kwargs):
        # 获取随机验证码
        regist_code = random.randint(100000, 1000000)
        # 保存到session中
        request.session['regist_code'] = str(regist_code)

        try:
            if request.session["logincount"] == 5:
                self.logincount = 5
                if datetime.datetime.now().strftime("%M") > request.session["nowtime"]:
                    request.session["logincount"] = 0
                    self.logincount = 0
        except:
            pass
        # 返回随机数
        return json_response({
            'regist_code': regist_code,
            "logincount": self.logincount
        })
