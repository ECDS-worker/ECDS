import os
from django.http import FileResponse
from api.comment import Rest
from EcdsApp.models import NetInfo,Commentuser,ApplyInfo,Insinfo, UserForm
from mailmerge import MailMerge


class AuditTable(Rest):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.username:
            username = request.session.get("username")
            user = Commentuser.objects.get(username=username)

        ins = Commentuser.objects.get(username=user.username).ins_id
        apply_info = ApplyInfo.objects.get(ins_id=ins)
        insname = Insinfo.objects.get(id=apply_info.ins_id)

        if apply_info.net_ty == 0:
            firewall = "√"
            softport = ""
        else:
            softport = "√"
            firewall = ""

        # 打印模板
        path = "media/upload/fulu/网络配置信息表.docx"
        # 创建邮件合并文档并查看所有字段
        document_1 = MailMerge(path)

        document_1.merge(
            ins_name=apply_info.ins.ins_nm,
            name=apply_info.contact_nm,
            phone=apply_info.phone,
            email=apply_info.email,
            firewall=firewall,
            softport=softport,
            IP_R2C1="",
            system_name="",
            pro_num="",
            ip="",
            laboratory_ip="",
            server_ip="",
            pro_EquiInfo=""
        )
        target = 'media/upload/fulu/'
        raw_name = insname.ins_nm + ".docx"
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(target)
        file_path = os.path.join(target, raw_name)
        document_1.write(file_path)

        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + raw_name
        return response
