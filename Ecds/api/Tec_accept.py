import os
from mailmerge import MailMerge
from django.http import FileResponse

from api.comment import Rest
from api.utils import json_response
from EcdsApp.models import SoftInfo, AcceptCheck, Commentuser
from api.decorators import commentuser_required


class TecAccept(Rest):
    """
            生成word模板
    """

    @commentuser_required
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        try:
            user = Commentuser.objects.get(username=username)
            ins_nm = user.ins.ins_nm
            acceptcheck = AcceptCheck.objects.get(ins_nm=ins_nm)
            softinfo = SoftInfo.objects.get(acceptcheck=acceptcheck)
        except Exception as e:
            return json_response({"msg": str(e)})

        # 打印模板
        path = "media/upload/apply_temp/技术验收软件信息表01.docx"
        # 创建邮件合并文档并查看所有字段
        document_1 = MailMerge(path)
        document_1.merge(
            ins_nm=ins_nm,
            company_adr=acceptcheck.company_adr,
            computer_adr=acceptcheck.computer_adr,
            zip_code=acceptcheck.zip_code,
            fax=acceptcheck.fax,
            contacts=acceptcheck.contacts,
            phone=acceptcheck.phone,
            email=acceptcheck.email,
            reply=acceptcheck.reply,
            soft_nm=softinfo.soft_nm,
            soft_ty=softinfo.soft_ty,
            database=softinfo.database,
            operat_sys=softinfo.operat_sys,
            cd_num=softinfo.cd_num,
            instruct_num=softinfo.instruct_num,
            enclosure_num=softinfo.enclosure_num,
            acces_sys=softinfo.acces_sys,
            acce_ty=acceptcheck.acce_ty,
            pro_line_num=softinfo.pro_line_num,
            pro_acc_num=softinfo.pro_acc_num,
            test_line_num=softinfo.test_line_num,
            test_acc_num=softinfo.test_acc_num,
            front_info=softinfo.front_info,
            MBFE=softinfo.MBFE,
            apply_mid=softinfo.apply_mid,
            message_mid=softinfo.message_mid,
        )
        target = 'media/upload/tec_accept/'
        raw_name = ins_nm + ".docx"
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(target)
        file_path = os.path.join(target, raw_name)
        document_1.write(file_path)

        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + raw_name
        return response
