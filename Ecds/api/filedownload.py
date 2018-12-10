import os
from django.http import FileResponse

from api.comment import Rest
from api.utils import *
from django.contrib.auth import get_user_model
from EcdsApp.models import UserForm, Commentuser
from api.decorators import ecdsuser_required, commentuser_required
User = get_user_model()


class UploadFile(Rest):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.username:
            username = request.session.get("username")
            user = Commentuser.objects.get(username=username)
        file_nm = UserForm.objects.filter(username=user.username).order_by("-id")[0].username
        return json_response({"file_nm": file_nm, "status": "200"})

    # @commentuser_required
    def put(self, request, *args, **kwargs):
        """文件下载   多接口调用，需要传递凭证，识别不同的表数据提取"""
        data = request.PUT
        filenm = data.get('filenm', '')
        try:
            url = UserForm.objects.get(filename=filenm).file_url
        except:
            return json_response({"msg": "无此文件"})
        file = open(url, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + filenm
        return response

    # @ecdsuser_required
    def post(self, request, *args, **kwargs):
        """文件上传"""
        user = request.user
        if not user.username:
            username = request.session.get("username")
            user = Commentuser.objects.get(username=username)
        user_up = UserForm()
        ret = {"status": "0"}
        target = "media/upload/avatar"  # 文件保存路径
        try:
            # 获取文件对象
            file_obj = request.FILES.get("file")
            raw_name = file_obj.name
        except Exception as e:
            ret["summary"] = str(e)
        else:
            if not file_obj:
                pass
            else:
                # 检查目录存不存在,如果不存在新建一个
                if not os.path.exists(os.path.dirname(target)):
                    os.makedirs(target)
                file_path = os.path.join(target, raw_name)
                with open(file_path, "wb") as f:
                    for chunk in file_obj.chunks():  # chuck是分块写入文件
                        f.write(chunk)
                ret["status"] = "200"

                """
                    机构名称存入对应的user信息中
                """
                try:
                    ins_nm = user.ins.ins_nm
                except:
                    ins_nm = user.ins

                user_up.username = user.username
                user_up.ins_nm = ins_nm
                user_up.file_url = file_path
                user_up.filename = raw_name
                user_up.save()
        return json_response(ret)
