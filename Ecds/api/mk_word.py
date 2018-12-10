from mailmerge import MailMerge
from EcdsApp.models import ApplyInfo, Commentuser
from api.comment import Rest
from django.http import FileResponse
from django.http import HttpResponse
from io import BytesIO
import os
import xlwt


class MakeWord(Rest):
    """
        生成word模板
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.username:
            username = request.session.get("username")
            user = Commentuser.objects.get(username=username)

        ins = Commentuser.objects.get(username=user.username).ins

        apply_ins = ApplyInfo.objects.get(ins=ins)

        if apply_ins.first_access == 1:
            fs = "■"
            sn = "□"
        else:
            fs = "□"
            sn = "▣"
        if apply_ins.net_ty == 0:
            net_ty_1 = "√"
            net_ty_2 = "×"
        else:
            net_ty_2 = "√"
            net_ty_1 = "×"

        # 打印模板
        path = "media/upload/apply_temp/申请信息模板.docx"

        # 创建邮件合并文档并查看所有字段

        document_1 = MailMerge(path)

        document_1.merge(
            ins_nm=ins.ins_nm,
            contact_nm=apply_ins.contact_nm,
            phone=apply_ins.phone,
            email=apply_ins.email,
            bank_num=apply_ins.bank_num,
            test_num=apply_ins.test_num,
            production_ccpc=apply_ins.production_ccpc,
            soft_nm=apply_ins.soft_nm,
            soft_type=apply_ins.soft_type,
            mid_message=apply_ins.mid_message,
            mid_apply=apply_ins.mid_apply,
            pro_version=apply_ins.pro_version,
            pro_system=apply_ins.pro_system,
            fs=fs,
            sn=sn,
            ins_mid=apply_ins.net_ty,
            net_ty_1=net_ty_1,
            net_ty_2=net_ty_2,
            access_obj=apply_ins.access_obj,
            start_time=apply_ins.start_time.strftime("%Y-%m-%d"),
            end_time=apply_ins.end_time.strftime("%Y-%m-%d")
        )
        target = 'media/upload/apply_info/'
        raw_name = ins.ins_nm+".docx"
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(target)
        file_path = os.path.join(target, raw_name)
        document_1.write(file_path)

        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + raw_name
        return response


class MakeExcel(Rest):
    """
        生成excel表格  申请者输出表
    """
    def post(self, request, *args, **kwargs):
        # 设置HTTPResponse的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=order.xls'
        # 创建一个文件对象
        wb = xlwt.Workbook(encoding='utf8')
        # 创建一个sheet对象
        sheet = wb.add_sheet('order-sheet')

        # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
        style_heading = xlwt.easyxf("""
                font:
                    name Arial,
                    colour_index white,
                    bold on,
                    height 0xA0;
                align:
                    wrap off,
                    vert center,
                    horiz center;
                pattern:
                    pattern solid,
                    fore-colour 0x19;
                borders:
                    left THIN,
                    right THIN,
                    top THIN,
                    bottom THIN;
                """)

        # 写入文件标题
        sheet.write(0, 0, '申请编号', style_heading)
        sheet.write(0, 1, '所属系统', style_heading)
        sheet.write(0, 2, '机构名', style_heading)
        for i in range(1, 13):
            sheet.write(0, i+2, str(i)+"月", style_heading)

        # 写入数据
        data_row = 1

        for i in ApplyInfo.objects.all():
            # 格式化datetime
            pri_time = int(i.start_time.strftime('%m'))
            # oper_time = int(i.end_time.strftime('%m'))
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, i.soft_nm)
            sheet.write(data_row, 2, i.operate_type)
            """
                单字段
            """
            for j in range(1, 13):
                moth = ""
                if pri_time == j:
                    moth = "√"
                sheet.write(data_row, j + 2, moth)
            """
                区间取值
            """
            # for j in range(1, 13):
            #     if j > pri_time:
            #         start = j
            #     else:
            #         start = pri_time
            #     for per_mo in range(start, oper_time+1):
            #         moth = ""
            #         if per_mo == j:
            #             moth = "√"
            #         sheet.write(data_row, j + 2, moth)
            #         break

            data_row = data_row + 1
        wb.save("media/upload/avatar/test2.xls")
        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
