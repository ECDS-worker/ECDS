from api.comment import Rest
import xlrd
from EcdsApp.models import NetInfo
from api.utils import json_response


class ExcelFile(Rest):
    def post(self, request, *args, **kwargs):
        data = request.POST
        url = data.get("url")
        # 打开文件
        data = xlrd.open_workbook(url)

        # 根据sheet名称获取
        sheet2 = data.sheet_by_name('Sheet1')
        nrows = sheet2.nrows   # 行
        ncols = sheet2.ncols   # 列

        # 循环行列表数据
        """
            可以前端传输一个数据，数据为已经搜索完成的字典数据,双层循环进行填写
        """
        for i in range(1, nrows):
            ip_r2c1 = sheet2.row_values(i)[0]
            server_ip = sheet2.row_values(i)[1]
            ins_nm = sheet2.row_values(i)[2]
            try:
                NetInfo.objects.get(ins_name=ins_nm)
            except Exception as e:
                return json_response({"msg": str(e), "error": ins_nm+"没执行完成"})
            else:
                NetInfo.objects.filter(ins_name=ins_nm).update(IP_R2C1=ip_r2c1, server_ip=server_ip)
        return json_response({"msg": "ok"})
