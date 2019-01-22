from EcdsApp.models import ApplyInfo, Commentuser, Insinfo, NetInfo, FornPro
from api.comment import Rest
from django.http import HttpResponse
from io import BytesIO
import xlwt
from api.utils import json_response
from datetime import datetime
from api.decorators import ecdsuser_release


def search(keyword, search_date, column, apply_info, retu_data):
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
    return apply_info


class MakeExcel(Rest):
    """
        生成excel表格  申请者输出表
        get, 生成excel
        post, 页面展示列表
        put, 展示单条详细信息
    """
    @ecdsuser_release
    def get(self, request, *args, **kwargs):
        user = request.user
        data = request.GET
        keyword = data.get("search_keyword", "")
        search_date = data.get("search_date", "")
        column = data.get("search_column", "")
        detailed = data.get("detail", "")

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
        style = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        style.alignment = al

        apply_info = []
        retu_data = {
            "retu_info": [],
            "status": "0"
        }
        search(keyword, search_date, column, apply_info, retu_data)

        if not detailed:
            # 写入文件标题
            sheet.write(0, 0, '申请编号', style_heading)
            sheet.write(0, 1, '所属系统', style_heading)
            sheet.write(0, 2, '机构名', style_heading)
            for i in range(1, 13):
                sheet.write(0, i + 2, str(i) + "月", style_heading)

            # 写出到IO
            data_row = 1
            for ai in apply_info:
                pri_time = int(ai.start_time.strftime('%m'))
                oper_time = int(ai.end_time.strftime('%m'))
                sheet.write(data_row, 0, ai.id, style)
                sheet.write(data_row, 1, ai.ins.ins_sysytem, style)
                sheet.write(data_row, 2, ai.ins.ins_nm, style)

                for j in range(1, 13):
                    if j > pri_time:
                        start = j
                    else:
                        start = pri_time
                    for per_mo in range(start, oper_time+1):
                        moth = ""
                        if per_mo == j:
                            moth = "√"
                        sheet.write(data_row, j + 2, moth, style)
                        break
                data_row += 1
        else:
            # 写入文件标题
            sheet.write(0, 0, '序号', style_heading)
            sheet.write(0, 1, '填报机构', style_heading)
            sheet.write(0, 2, '网络运维联系人', style_heading)
            sheet.write(0, 3, '角色', style_heading)
            sheet.write(0, 4, '电话', style_heading)
            sheet.write(0, 5, '邮箱', style_heading)
            sheet.write(0, 6, '参与者VPN介入类型', style_heading)
            sheet.write(0, 7, 'VPN接入设备公网地址', style_heading)
            sheet.write(0, 8, '接入业务系统名称', style_heading)
            sheet.write(0, 9, '业务前置机数量', style_heading)
            sheet.write(0, 10, '参与者外联通信IP地址R2C1', style_heading)
            sheet.write(0, 11, 'VPN实验室测试环境设备公网地址', style_heading)
            sheet.write(0, 12, '系统联调测试实验室服务器外部通信地址', style_heading)
            sheet.write(0, 13, '参与者VPN接入设备信息', style_heading)
            sheet.write(0, 14, '测试机构名称', style_heading)
            sheet.write(0, 15, '测试机构行号', style_heading)
            sheet.write(0, 16, '接入ECDS方式', style_heading)
            sheet.write(0, 17, '测试环境接入点号', style_heading)
            sheet.write(0, 18, '测试CCPC', style_heading)
            sheet.write(0, 19, '生产环境接入点号', style_heading)
            sheet.write(0, 20, '生产CCPC', style_heading)
            sheet.write(0, 21, '中间件类型', style_heading)
            sheet.write(0, 22, '中间件版本', style_heading)
            sheet.write(0, 23, '队列管理器名称', style_heading)
            sheet.write(0, 24, '前置机版本', style_heading)
            sheet.write(0, 25, '前置机操作系统平台', style_heading)
            sheet.write(0, 26, '申请月份', style_heading)
            sheet.write(0, 27, '申请月份负责人', style_heading)

            # 写出到IO
            data_row = 1
            for ai in apply_info:
                netinfo = NetInfo.objects.get(aply_info=ai)
                for_pro = FornPro.objects.get(aply_info=ai)
                name = role = phone = email = ""
                sheet.write(data_row, 0, ai.id)
                sheet.write(data_row, 1, ai.ins.ins_nm)
                for items in ai.ins.contactsinfo_set.all():
                    name = name+"\n"+items.name
                    role = role+"\n"+items.role
                    phone = phone+"\n"+items.phone
                    email = email+"\n"+items.email
                sheet.write(data_row, 2, name)
                sheet.write(data_row, 3, role)
                sheet.write(data_row, 4, phone)
                sheet.write(data_row, 5, email)
                sheet.write(data_row, 6, ai.net_ty)
                sheet.write(data_row, 7, netinfo.ip)
                sheet.write(data_row, 8, netinfo.system_name)
                sheet.write(data_row, 9, netinfo.pro_num)
                sheet.write(data_row, 10, netinfo.IP_R2C1)
                sheet.write(data_row, 11, netinfo.laboratory_ip)
                sheet.write(data_row, 12, netinfo.server_ip)
                sheet.write(data_row, 13, netinfo.pro_EquiInfo)
                sheet.write(data_row, 14, ai.ins.ins_nm)
                sheet.write(data_row, 15, ai.bank_num)
                sheet.write(data_row, 16, ai.acc_ecds)
                sheet.write(data_row, 17, ai.test_num)
                sheet.write(data_row, 18, ai.test_ccpc)
                sheet.write(data_row, 19, ai.product_num)
                sheet.write(data_row, 20, ai.production_ccpc)
                sheet.write(data_row, 21, ai.mid_message)
                sheet.write(data_row, 22, ai.mid_apply)
                sheet.write(data_row, 23, for_pro.port)
                sheet.write(data_row, 24, for_pro.pro_version)
                sheet.write(data_row, 25, for_pro.pro_system)
                sheet.write(data_row, 26, ai.acc_month)
                sheet.write(data_row, 27, ai.support_name)
                data_row += 1
        wb.save("media/upload/avatar/test1.xls")

        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response

    @ecdsuser_release
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.POST
        keyword = data.get("search_keyword", "")
        search_date = data.get("search_date", "")
        column = data.get("search_column", "")
        apply_info = []
        retu_data = {
            "retu_info": [],
            "status": "0"
        }
        search(keyword, search_date, column, apply_info, retu_data)

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

    @ecdsuser_release
    def put(self, request, *args, **kwargs):
        """
            查询详细信息
        """
        user = request.user
        data = request.PUT
        keyword = data.get("search_keyword", "")
        search_date = data.get("search_date", "")
        column = data.get("search_column", "")
        retu_data = {
            "retu_info": [],
            "status": "0"
        }

        apply_info = []
        search(keyword, search_date, column, apply_info, retu_data)
        for ai in apply_info:
            retu_dic = dict()
            netinfo = NetInfo.objects.get(aply_info=ai)
            for_pro = FornPro.objects.get(aply_info=ai)

            retu_dic["id"] = ai.id
            retu_dic["ins_nm"] = ai.ins.ins_nm
            retu_dic["contact"] = [{
                "name": items.name,
                "role": items.role,
                "phone": items.phone,
                "email": items.email
            } for items in ai.ins.contactsinfo_set.all()]
            retu_dic["net_ty"] = ai.net_ty
            retu_dic["IP_R2C1"] = netinfo.ip
            retu_dic["system_name"] = netinfo.system_name
            retu_dic["pro_num"] = netinfo.pro_num
            retu_dic["ip"] = netinfo.IP_R2C1
            retu_dic["laboratory_ip"] = netinfo.laboratory_ip
            retu_dic["server_ip"] = netinfo.server_ip
            retu_dic["pro_EquiInfo"] = netinfo.pro_EquiInfo
            retu_dic["test_ins"] = ai.ins.ins_nm
            retu_dic["bank_num"] = ai.bank_num
            retu_dic["acc_ecds"] = ai.acc_ecds
            retu_dic["test_num"] = ai.test_num
            retu_dic["test_ccpc"] = ai.test_ccpc
            retu_dic["product_num"] = ai.product_num
            retu_dic["production_ccpc"] = ai.production_ccpc
            retu_dic["mid_message"] = ai.mid_message
            retu_dic["mid_apply"] = ai.mid_apply
            retu_dic["port"] = for_pro.port
            retu_dic["pro_version"] = for_pro.pro_version
            retu_dic["pro_system"] = for_pro.pro_system
            retu_dic["acc_month"] = ai.acc_month
            retu_dic["support_name"] = ai.support_name

            retu_data["retu_info"].append(retu_dic)
        return json_response(retu_data)
