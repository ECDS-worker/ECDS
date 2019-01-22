from api.comment import Rest
from EcdsApp.models import *
from django.http import HttpResponse
from io import BytesIO
from api.utils import json_response
import xlwt
from datetime import datetime
# from api.decorators import ecdsuser_required, commentuser_required


class Search(Rest):
    def put(self, request, *args, **kwargs):
        # user = request.user
        # if not user.username:
        #     username = request.session.get("username")
        #     user = Commentuser.objects.get(username=username)
        data = request.PUT
        keyword = data.get("search_keyword", "")
        search_date = data.get("search_date", "")
        column = data.get("search_column", "")
        retu_data = {
            "retu_info": [],
            "status": "0"
        }
        apply_info = []
        try:
            if keyword:
                all_ins = Insinfo.objects.filter(ins_nm__contains=keyword)
                for per_ins in all_ins:
                    try:
                        apply = ApplyInfo.objects.get(activate=1, ins=per_ins)
                        apply_info.append(apply)
                    except:
                        pass
            if search_date:
                start_date = datetime.strptime(search_date.split()[0], '%Y-%m-%d')
                end_date = datetime.strptime(search_date.split()[2], '%Y-%m-%d')
                if apply_info:
                    for per_ins in apply_info:
                        if not (per_ins.start_time >= start_date and per_ins.end_time <= end_date):
                            apply_info.remove(per_ins)
                else:
                    apply_info = ApplyInfo.objects.filter(activate=1, start_time__gte=start_date,
                                                          end_time__lte=end_date)

            if column:
                if apply_info:
                    for per_ins in apply_info:
                        if per_ins.operating != column:
                            apply_info.remove(per_ins)
                else:
                    apply_info = ApplyInfo.objects.filter(operating__contains=column)
            retu_data["status"] = "200"
        except Exception as e:
            return json_response({"msg": str(e)})

        first_acc = "是"

        for ai in apply_info:
            retu_dic = dict()
            retu_dic["id"] = ai.id
            # retu_dic["operating"] = ai.operating
            retu_dic["ins_nm"] = ai.ins.ins_nm
            if ai.first_access == 0:
                first_acc = "否"
            retu_dic["first_acc"] = first_acc
            retu_dic["ins_cd"] = ai.ins.ins_cd
            retu_dic["access_port"] = ai.ins.access_port
            retu_dic["pro_CCPC"] = ""
            # retu_dic["ins_mid"] = ai.ins.ins_mid
            retu_dic["test_port"] = ""
            retu_dic["date"] = ai.start_time.strftime("%Y-%m")
            retu_dic["test_CCPC"] = ""
            retu_data["retu_info"].append(retu_dic)

        return json_response(retu_data)

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.username:
            username = request.session.get("username")
            user = Commentuser.objects.get(username=username)
        data = request.GET
        keyword = data.get("search_keyword", "")
        search_date = data.get("search_date", "")
        column = data.get("search_column", "")

        # 设置HTTPResponse的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=search.xls'
        # 创建一个文件对象
        wb = xlwt.Workbook(encoding='utf8')
        # 创建一个sheet对象
        sheet = wb.add_sheet('order-sheet')

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
        sheet.write(0, 0, '编号', style_heading)
        sheet.write(0, 1, '所属系统', style_heading)
        sheet.write(0, 2, '机构名', style_heading)
        sheet.write(0, 3, '是否首次接入', style_heading)
        sheet.write(0, 4, '行号', style_heading)
        sheet.write(0, 5, '生产环境接入点号', style_heading)
        sheet.write(0, 6, '生产CCPC', style_heading)
        sheet.write(0, 7, 'MQ/TLQ', style_heading)
        sheet.write(0, 8, '测试环境接入点号', style_heading)
        sheet.write(0, 9, '申请时段', style_heading)
        sheet.write(0, 10, '测试CCPC', style_heading)

        apply_info = []
        try:
            if keyword:
                all_ins = Insinfo.objects.filter(ins_nm__contains=keyword)
                for per_ins in all_ins:
                    apply = ApplyInfo.objects.get(activate=1, ins=per_ins)
                    apply_info.append(apply)
            if search_date:
                start_date = datetime.strptime(search_date.split()[0], '%Y-%m-%d')
                end_date = datetime.strptime(search_date.split()[2], '%Y-%m-%d')
                if apply_info:
                    for per_ins in apply_info:
                        if not (per_ins.start_time >= start_date and per_ins.end_time <= end_date):
                            apply_info.remove(per_ins)
                else:
                    apply_info = ApplyInfo.objects.filter(activate=1, start_time__gte=start_date, end_time__lte=end_date)
            if column:
                if apply_info:
                    for per_ins in apply_info:
                        if per_ins.operating != column:
                            apply_info.remove(per_ins)
                else:
                    apply_info = ApplyInfo.objects.filter(operating__contains=column)
        except Exception as e:
            return json_response({"msg": e})
        # 写出到IO
        data_row = 1
        first_acc = "是"
        for ai in apply_info:
            sheet.write(data_row, 0, ai.id)
            sheet.write(data_row, 1, ai.operating)
            sheet.write(data_row, 2, ai.ins.ins_nm)
            if ai.first_access == 0:
                first_acc = "否"
            sheet.write(data_row, 3, first_acc)
            sheet.write(data_row, 4, ai.ins.ins_cd)
            sheet.write(data_row, 5, ai.ins.access_port)
            sheet.write(data_row, 6, "")
            sheet.write(data_row, 7, ai.ins.ins_mid)
            sheet.write(data_row, 8, "")
            sheet.write(data_row, 9, ai.start_time.strftime("%Y-%m"))
            sheet.write(data_row, 10, "")
            data_row += 1
        wb.save("media/upload/avatar/test1.xls")

        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
