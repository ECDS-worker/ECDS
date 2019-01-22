import xlwt
from django.http import HttpResponse
from io import BytesIO
from django.core.paginator import Paginator, EmptyPage

from api.comment import Rest
from api.utils import json_response
from datetime import datetime
from EcdsApp.models import Insinfo, AcceptCheck, SoftInfo
from api_ecds.email import email


def search(keyword, search_date, accept_info, retu_data):
    try:
        if keyword:
            all_ins = Insinfo.objects.filter(ins_nm__contains=keyword)
            for per_ins in all_ins:
                try:
                    apply = AcceptCheck.objects.get(check_state=0, ins_nm=per_ins.ins_nm)
                    accept_info.append(apply)
                except:
                    pass
        if search_date:
            start_date = datetime.strptime(search_date.split()[0], '%Y-%m-%d')
            end_date = datetime.strptime(search_date.split()[2], '%Y-%m-%d')
            if accept_info:
                for per_ins in accept_info:
                    if not (per_ins.start_time >= start_date and per_ins.end_time <= end_date):
                        accept_info.remove(per_ins)
            else:
                accept_info = AcceptCheck.objects.filter(check_state=0, apply_date__gte=start_date,
                                                            apply_date__lte=end_date)
    except Exception as e:
        return json_response({"msg": str(e)})

    if not accept_info:
        return json_response(retu_data)
    return accept_info


class CheckApply(Rest):
    """
        get, 页面展示列表
        put, 展示单条详细信息
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        retu_data = {
            "retu_info": [],
            "page_nums": "",
        }
        accept_info = AcceptCheck.objects.filter(check_state=0)
        if not accept_info:
            return json_response(retu_data)

        # 构建分页器对象,cur_apply=所有数据,2=每页显示的个数
        paginator = Paginator(accept_info, 10)
        num_page = request.GET.get("page", 1)
        page_nu = paginator.count
        retu_data["page_nums"] = page_nu
        try:
            content = paginator.page(num_page)
        except EmptyPage:
            content = paginator.page(paginator.num_pages)
        for acceptcheck in content.object_list:
            try:
                soft_info = SoftInfo.objects.get(acceptcheck=acceptcheck)
            except Exception as e:
                return json_response({"msg": str(e)})
            retu_dic = {
                "id": acceptcheck.id,
                "ins_nm": acceptcheck.ins_nm,
                "reply": acceptcheck.reply,
                "contacts": acceptcheck.contacts,
                "phone": acceptcheck.phone,
                "email": acceptcheck.email,
                "computer_adr": acceptcheck.computer_adr,
                "company_adr": acceptcheck.company_adr,
                "zip_code": acceptcheck.zip_code,
                "fax": acceptcheck.fax,
                "soft_nm": soft_info.soft_nm,
                "soft_ty": soft_info.soft_ty,
                "mid_ty": soft_info.mid_ty,
                "database": soft_info.database,
                "operat_sys": soft_info.operat_sys,
                "cd_num": soft_info.cd_num,
                "instruct_num": soft_info.instruct_num,
                "enclosure_num": soft_info.enclosure_num,
                "acces_sys": soft_info.acces_sys,
                "acce_ty": soft_info.acces_type,
                "test_descrip": soft_info.test_descrip
            }
            retu_data["retu_info"].append(retu_dic)
            retu_data["status"] = "200"
        return json_response(retu_data)

    def put(self, request, *args, **kwargs):
        """
            单条查询详细信息
            传入当前点击的机构名称  可换成机构号
            传入整形数字为参照，0、1、2、   详情、通过、退回
        """
        user = request.user
        data = request.PUT
        ins_nm = data.get("keyword", "")
        state = data.get("state", 0)

        retu_data = dict()
        try:
            acceptcheck = AcceptCheck.objects.get(ins_nm=ins_nm, check_state=0)
        except Exception as e:
            return json_response({"msg": str(e)})
        if state == 0:
            if acceptcheck:
                try:
                    soft_info = SoftInfo.objects.get(acceptcheck=acceptcheck)
                except Exception as e:
                    return json_response({"msg": str(e)})
                retu_data = {
                    "id": acceptcheck.id,
                    "ins_nm": acceptcheck.ins_nm,
                    "reply": acceptcheck.reply,
                    "contacts": acceptcheck.contacts,
                    "phone": acceptcheck.phone,
                    "email": acceptcheck.email,
                    "computer_adr": acceptcheck.computer_adr,
                    "company_adr": acceptcheck.company_adr,
                    "zip_code": acceptcheck.zip_code,
                    "fax": acceptcheck.fax,
                    "soft_nm": soft_info.soft_nm,
                    "soft_ty": soft_info.soft_ty,
                    "mid_ty": soft_info.mid_ty,
                    "database": soft_info.database,
                    "operat_sys": soft_info.operat_sys,
                    "cd_num": soft_info.cd_num,
                    "instruct_num": soft_info.instruct_num,
                    "enclosure_num": soft_info.enclosure_num,
                    "acces_sys": soft_info.acces_sys,
                    "acce_ty": soft_info.acces_type,
                    "test_descrip": soft_info.test_descrip
                }
        elif state == 1:
            acceptcheck.check_state = 1
            acceptcheck.save()
            username_recv = acceptcheck.email
            content = "您所提交的测试申请以审核成功，请注意查看官网动态"
            email(username_recv, content)
            retu_data["state"] = "200"
        else:
            acceptcheck.check_state = 2
            acceptcheck.save()
            username_recv = acceptcheck.email
            content = "您所提交的测试申请被退回，请注意查看官网动态"
            email(username_recv, content)
            retu_data["state"] = "200"
        return json_response(retu_data)


class CheckSearch(Rest):
    """
        搜索接入技术验收信息
        get, 生成excel
        post, 展示搜索详细信息
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        data = request.GET
        keyword = data.get("search_keyword", "")
        search_date = data.get("search_date", "")
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

        accept_info = []
        retu_data = {
            "retu_info": [],
            "status": "0"
        }

        # 写入文件标题
        sheet.write_merge(0, 1, 0, 0, '序号', style_heading)
        sheet.write_merge(0, 1, 1, 1, '参与机构名称', style_heading)
        sheet.write_merge(0, 1, 2, 2, '介入类型', style_heading)
        sheet.write_merge(0, 1, 3, 3, '专线情况', style_heading)
        sheet.write_merge(0, 1, 4, 4, '申请日期', style_heading)
        sheet.write_merge(0, 1, 5, 5, '批复文件', style_heading)
        sheet.write_merge(0, 1, 6, 6, '是否至少测试一月', style_heading)
        sheet.write_merge(0, 0, 7, 12, '待验收项', style_heading)
        sheet.write_merge(0, 1, 13, 13, '区域', style_heading)
        sheet.write_merge(0, 1, 14, 14, '城市', style_heading)
        sheet.write_merge(0, 1, 15, 15, '联系人', style_heading)
        sheet.write_merge(0, 1, 16, 16, '联系电话', style_heading)
        sheet.write_merge(0, 1, 17, 17, '邮箱', style_heading)
        sheet.write_merge(0, 1, 18, 18, '机房地址', style_heading)
        sheet.write(1, 7, "接入端软件检测", style_heading)
        sheet.write(1, 8, "验收时间", style_heading)
        sheet.write(1, 9, "接入端信息系统检查", style_heading)
        sheet.write(1, 10, "验收时间", style_heading)
        sheet.write(1, 11, "接入环境检查", style_heading)
        sheet.write(1, 12, "验收时间", style_heading)

        res_list = search(keyword, search_date, accept_info, retu_data)
        data_row = 2
        for ai in res_list:
            sheet.write(data_row, 0, ai.id)
            sheet.write(data_row, 1, ai.ins_nm)
            sheet.write(data_row, 2, ai.acce_ty)
            sheet.write(data_row, 3, ai.dedicated)
            sheet.write(data_row, 4, ai.apply_date.strftime("%Y-%m-%d"))
            sheet.write(data_row, 5, ai.reply)
            sheet.write(data_row, 6, ai.all_month)
            sheet.write(data_row, 7, ai.acces_detec)
            sheet.write(data_row, 8, ai.check_time1.strftime("%Y-%m-%d"))
            sheet.write(data_row, 9, ai.acces_info)
            sheet.write(data_row, 10, ai.check_time2.strftime("%Y-%m-%d"))
            sheet.write(data_row, 11, ai.env_check)
            sheet.write(data_row, 12, ai.check_time3.strftime("%Y-%m-%d"))
            sheet.write(data_row, 13, ai.region)
            sheet.write(data_row, 14, ai.city)
            sheet.write(data_row, 15, ai.contacts)
            sheet.write(data_row, 16, ai.phone)
            sheet.write(data_row, 17, ai.email)
            sheet.write(data_row, 18, ai.computer_adr)
            sheet.write(data_row, 19, ai.company_adr)
            sheet.write(data_row, 20, ai.zip_code)
            sheet.write(data_row, 21, ai.fax)
            sheet.write(data_row, 22, ai.check_state)

            data_row += 1

        wb.save("media/upload/avatar/accept_check.xls")
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
        accept_info = []
        retu_data = {
            "retu_info": [],
            "page_nums": "",
        }
        # search(keyword, search_date, accept_info, retu_data)
        if keyword:
            all_ins = Insinfo.objects.filter(ins_nm__contains=keyword)
            for per_ins in all_ins:
                try:
                    apply = AcceptCheck.objects.get(check_state=0, ins_nm=per_ins.ins_nm)
                    accept_info.append(apply)
                except:
                    pass
        if search_date:
            start_date = datetime.strptime(search_date.split()[0], '%Y-%m-%d')
            end_date = datetime.strptime(search_date.split()[2], '%Y-%m-%d')
            if accept_info:
                for per_ins in accept_info:
                    if not (per_ins.apply_date >= start_date or per_ins.apply_date <= end_date):
                        accept_info.remove(per_ins)
            else:
                accept_info = AcceptCheck.objects.filter(check_state=0, apply_date__gte=start_date,
                                                         apply_date__lte=end_date)

        # 构建分页器对象,cur_apply=所有数据,2=每页显示的个数
        paginator = Paginator(accept_info, 19)
        num_page = request.GET.get("page", 1)
        page_nu = paginator.count
        retu_data["page_nums"] = page_nu
        try:
            content = paginator.page(num_page)
        except EmptyPage:
            content = paginator.page(paginator.num_pages)
        for acceptcheck in content.object_list:
            retu_dic = {
                "id": acceptcheck.id,
                "ins_nm": acceptcheck.ins_nm,
                "acce_ty": acceptcheck.acce_ty,
                "dedicated": acceptcheck.dedicated,
                "apply_date": acceptcheck.apply_date.strftime("%Y-%m-%d"),
                "reply": acceptcheck.reply,
                "all_month": acceptcheck.reply,
                "acces_detec": acceptcheck.acces_detec,
                "check_time1": acceptcheck.check_time1.strftime("%Y-%m-%d"),
                "acces_info": acceptcheck.acces_info,
                "check_time2": acceptcheck.check_time2.strftime("%Y-%m-%d"),
                "env_check": acceptcheck.env_check,
                "check_time3": acceptcheck.check_time3.strftime("%Y-%m-%d"),
                "region": acceptcheck.region,
                "city": acceptcheck.city,
                "contacts": acceptcheck.contacts,
                "phone": acceptcheck.phone,
                "email": acceptcheck.email,
                "computer_adr": acceptcheck.computer_adr,
                "company_adr": acceptcheck.company_adr,
                "zip_code": acceptcheck.company_adr,
                "fax": acceptcheck.fax,
                "check_state": acceptcheck.check_state
            }
            retu_data["retu_info"].append(retu_dic)
            retu_data["status"] = "200"
        return json_response(retu_data)