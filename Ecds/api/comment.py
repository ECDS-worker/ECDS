import random
import json
from datetime import datetime

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login


from api.utils import *
from EcdsApp.models import *
# from api.decorators import *


class Rest(object):
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__.lower()
        # 定义一个方法，用于绑定到url

    @csrf_exempt
    def enter(self, request, *args, **kwargs):
        # 取出客户端请求方法
        method = request.method
        # 根据请求方法执行相应的处理函数
        if method == 'GET':
            # 获取资源
            return self.get(request, *args, **kwargs)
        elif method == 'POST':
            # 新增资源
            return self.post(request, *args, **kwargs)
        elif method == 'PUT':
            # 更新资源
            return self.put(request, *args, **kwargs)
        elif method == 'DELETE':
            # 删除资源
            return self.delete(request, *args, **kwargs)
        else:
            # 不支持其他请求方法
            return method_not_allowed()

    def get(self, request, *args, **kwargs):
        return method_not_allowed()

    def post(self, request, *args, **kwargs):
        return method_not_allowed()

    def put(self, request, *args, **kwargs):
        return method_not_allowed()

    def delete(self, request, *args, **kwargs):
        return method_not_allowed()


class Register(object):
    def __init__(self):
        self.resources = []

    def regist(self, resource):
        self.resources.append(resource)

    @property
    def urls(self):
        # 路由注册
        urlpatterns = [
            url(r'^{name}$'.format(name=resource.name), resource.enter) for resource in self.resources
        ]
        return urlpatterns
