import json

from django.utils.deprecation import MiddlewareMixin

from api.utils import params_error


class ConvertData(MiddlewareMixin):
    def process_request(self, request):
        # 判断是否使用的是get方法，如果是，直接返回
        method = request.method
        if method == "GET":
            return None
        if method == "POST":
            if 'application/json' not in request.content_type:
                return None
        if 'application/json' in request.content_type:
            try:
                data = json.loads(request.body.decode())
            except Exception:
                return params_error({
                    "msg": "json数据格式有误"
                })
        else:
            return params_error({
                "msg": "请提交json数据类型"
            })
        setattr(request, method, data)
