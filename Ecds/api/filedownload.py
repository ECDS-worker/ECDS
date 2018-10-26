from datetime import time, datetime
import os
import uuid
from django.http import StreamingHttpResponse
from django.http import FileResponse

from api.comment import Rest
from api.utils import *
from EcdsApp.models import UserForm
from api.decorators import customer_required


class UploadFile(Rest):
    @customer_required
    def get(self, request, *args, **kwargs):
        """文件下载"""
        file = open('media/upload/avatar/req.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="xlsx_file.xlsx"'
        return response

    @customer_required
    def post(self, request, *args, **kwargs):
        """文件上传"""
        user_up = UserForm()
        user_up.username = request.user.username
        ret = {"status": False, "data": {"path": "", "name": ""}, "summary": ""}
        target = "media/upload/avatar"  # 文件保存路径
        try:
            # 获取文件对象
            file_obj = request.FILES.get("file")
            raw_name = file_obj.name
            if not file_obj:
                pass
            else:
                # 检查目录存不存在,如果不存在新建一个
                if not os.path.exists(os.path.dirname(target)):
                    os.makedirs(target)
                file_name = str(uuid.uuid4())
                file_path = os.path.join(target, file_name)
                with open(file_path, "wb") as f:
                    for chunk in file_obj.chunks():  # chuck是分块写入文件 （.chunks()上循环而不是用read()保证大文件不会大量使用你的系统内存。）
                        f.write(chunk)
                ret["status"] = True
                ret["data"]['path'] = file_path
                ret["data"]['name'] = raw_name
                user_up.fileurl = file_path
                user_up.save()
        except Exception as e:
            ret["summary"] = str(e)
        return json_response(ret)
