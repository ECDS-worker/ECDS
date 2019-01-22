import xlwt
import os
from django.http import HttpResponse
from io import BytesIO
from datetime import datetime

from EcdsApp.models import NetInfo, ApplyInfo, Insinfo, TestFile
from api.utils import json_response
from api.comment import Rest


class AcceptRecord(Rest):
    """
        生成excel表格  申请者输出表
    """
    def get(self, request, *args, **kwargs):
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

        wb.save("media/upload/avatar/mk_excel.xls")
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response


class TestingFile(Rest):
    """
        接入软件检测相关文档
        get, 文档信息展示
        post，文档上传
        put, 文档更新
        delete， 删除相关文档
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        now_time = datetime.now()
        try:
            all_txt = TestFile.objects.filter(end_time__gte=now_time)
        except Exception as e:
            return json_response({"msg": str(e)})
        retu_data = dict()
        retu_data["user_nm"] = user.username
        retu_data["file_text"] = [{
            "file_name": item.file_nm,
            "date": item.up_date.strftime("%Y-%m-%d"),
            "up_user": item.up_user,
            "status": item.check_status
        } for item in all_txt]
        return json_response(retu_data)

    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args: end_time(有效时间)， up_type（上传功能传参数， 更新时不传参） file_name(更新时传递此参数，文件名称)
        """
        user = request.user
        end_time = request.POST.get("end_time")
        up_type = request.POST.get("up_type", "")

        ret = {"status": "0"}
        target = "media/upload/testing/"

        try:
            # 获取文件对象
            file_obj = request.FILES.get("file")
            raw_name = file_obj.name
        except Exception as e:
            ret["summary"] = str(e)
        else:

            # 检查目录存不存在,如果不存在新建一个
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(target)
            file_path = os.path.join(target, raw_name)
            with open(file_path, "wb") as f:
                for chunk in file_obj.chunks():  # chuck是分块写入文件
                    f.write(chunk)
            ret["status"] = "200"

            if up_type:
                try:
                    TestFile.objects.get(up_user=user.username, file_nm=raw_name)
                except:
                    test_file = TestFile()
                    test_file.up_user = user
                    test_file.file_nm = raw_name
                    test_file.file_url = file_path
                    test_file.end_time = end_time
                    test_file.save()
                    ret["msg"] = "上传成功"
                else:
                    return json_response({"msg": "此文件已存在"})
            else:
                file_name = request.POST.get("file_nm", "")
                try:
                    TestFile.objects.filter(up_user=user, file_nm=file_name).update(file_nm=raw_name, file_url=file_path)
                    ret["msg"] = "更新成功"
                except Exception as e:
                    return json_response({"msg": str(e)})

        return json_response(ret)

    def delete(self, request, *args, **kwargs):
        user = request.user
        file_name = request.DELETE.get("file_nm", "")
        try:
            file_obj = TestFile.objects.get(file_nm=file_name)
            os.remove(file_obj.file_url)
            TestFile.objects.get(file_nm=file_name).delete()
            return json_response({"msg": "删除成功"})
        except Exception as e:
            return json_response({"msg": str(e)})
