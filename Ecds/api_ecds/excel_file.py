import xlrd
import os
from datetime import datetime

from EcdsApp.models import NetInfo, ApplyInfo, Insinfo
from api.utils import json_response
from api.comment import Rest
from api.decorators import ecdsuser_input


class ExcelFile(Rest):
    # @ecdsuser_input
    def post(self, request, *args, **kwargs):
        """
        使用excel表批量导入两个ip字段
        ip_type   不传则为分配ip, 传值则为分配测试号
        """
        data = request.POST
        ip_type = data.get("ip_type", "")
        ret = {"status": "0"}

        try:
            # 获取文件对象
            file_obj = request.FILES.get("file")
            raw_name = file_obj.name
        except Exception as e:
            ret["summary"] = str(e)
            return json_response(ret)

        target = "media/upload/excel"  # 文件保存路径
        # 检查目录存不存在,如果不存在新建一个
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(target)
        file_path = os.path.join(target, raw_name)
        with open(file_path, "wb") as f:
            for chunk in file_obj.chunks():  # chuck是分块写入文件
                f.write(chunk)
        ret["status"] = "200"

        # 打开文件
        data = xlrd.open_workbook(file_path)

        # 根据sheet名称获取
        sheet2 = data.sheet_by_name('Sheet1')
        nrows = sheet2.nrows   # 行
        # ncols = sheet2.ncols   # 列

        # 循环行列表数据
        """
            可以前端传输一个数据，数据为已经搜索完成的字典数据,双层循环进行填写
        """
        if not ip_type:
            for i in range(1, nrows):
                ins_nm = sheet2.row_values(i)[2]
                try:
                    NetInfo.objects.get(ins_nm=ins_nm)
                except:
                    pass
                else:
                    ip_r2c1 = sheet2.row_values(i)[0]
                    server_ip = sheet2.row_values(i)[1]
                    NetInfo.objects.filter(ins_nm=ins_nm).update(IP_R2C1=ip_r2c1, server_ip=server_ip)
                    ins = Insinfo.objects.get(ins_nm=ins_nm)
                    ApplyInfo.objects.filter(ins=ins).update(check_state=2)
        else:
            now_time = datetime.now().strftime("%m")
            for i in range(1, nrows):
                bank_num = str(int(sheet2.row_values(i)[2]))
                try:
                    ApplyInfo.objects.get(bank_num=bank_num, acc_month=now_time)
                except:
                    pass
                else:
                    test_num = sheet2.row_values(i)[0]
                    test_ccpc = sheet2.row_values(i)[1]
                    ApplyInfo.objects.filter(bank_num=bank_num, acc_month=now_time).update(test_num=test_num, test_ccpc=test_ccpc, check_state=3)
        return json_response({"msg": "ok"})
