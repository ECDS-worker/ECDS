from EcdsApp.models import ApplyInfo, Commentuser, Insinfo
from api.comment import Rest
from django.http import HttpResponse
from io import BytesIO
import xlwt
from api.utils import json_response
from datetime import datetime
from api.decorators import ecdsuser_required, commentuser_required


class MakeExcel(Rest):
    """
        生成excel表格  申请者输出表
    """
    def get(self, request, *args, **kwargs):
        user = request.user
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
        sheet.write(0, 0, '申请编号', style_heading)
        sheet.write(0, 1, '所属系统', style_heading)
        sheet.write(0, 2, '机构名', style_heading)
        for i in range(1, 13):
            sheet.write(0, i + 2, str(i) + "月", style_heading)

        apply_info = []
        try:
            if keyword:
                all_ins = Insinfo.objects.filter(ins_nm__contains=keyword)
                for per_ins in all_ins:
                    try:
                        apply = ApplyInfo.objects.get(check_state=1, ins=per_ins)
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
                    apply_info = ApplyInfo.objects.filter(check_state=1, start_time__gte=start_date, end_time__lte=end_date)
            if column:
                if apply_info:
                    for per_ins in apply_info:
                        if per_ins.operating != column:
                            apply_info.remove(per_ins)
                else:
                    apply_info = ApplyInfo.objects.filter(operating__contains=column)
        except Exception as e:
            return json_response({"msg": str(e)})
        if not apply_info:
            return json_response({"msg": "无数据"})
        # 写出到IO
        data_row = 1
        for ai in apply_info:
            pri_time = int(ai.start_time.strftime('%m'))
            oper_time = int(ai.end_time.strftime('%m'))
            sheet.write(data_row, 0, ai.id)
            sheet.write(data_row, 1, ai.soft_nm)
            sheet.write(data_row, 2, ai.ins.ins_sysytem)

            for j in range(1, 13):
                if j > pri_time:
                    start = j
                else:
                    start = pri_time
                for per_mo in range(start, oper_time+1):
                    moth = ""
                    if per_mo == j:
                        moth = "√"
                    sheet.write(data_row, j + 2, moth)
                    break
            data_row += 1
        wb.save("media/upload/avatar/test1.xls")

        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.POST
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
                        apply = ApplyInfo.objects.get(check_state=1, ins=per_ins)
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
                    apply_info = ApplyInfo.objects.filter(check_state=1, start_time__gte=start_date,
                                                          end_time__lte=end_date)
            if column:
                if apply_info:
                    for per_ins in apply_info:
                        if per_ins.operating != column:
                            apply_info.remove(per_ins)
                else:
                    apply_info = ApplyInfo.objects.filter(operating__contains=column)
        except Exception as e:
            return json_response({"msg": str(e)})
        if not apply_info:
            return json_response(retu_data)

        for ai in apply_info:
            pri_time = int(ai.start_time.strftime('%m'))
            retu_dic = dict()
            retu_dic["id"] = ai.id
            retu_dic["ins_nm"] = ai.ins.ins_nm
            retu_dic["ins_sysytem"] = ai.ins.ins_sysytem
            for j in range(1, 13):
                if j > pri_time:
                    start = j
                else:
                    start = pri_time
                for per_mo in range(start, 14):
                    month = ""
                    if per_mo == j:
                        month = "√"
                    retu_dic[str(j)] = month
                    break
            retu_data["retu_info"].append(retu_dic)
        return json_response(retu_data)
