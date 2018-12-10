import re
from django.http import FileResponse
from api.comment import Rest
from EcdsApp.models import ApplyInfo, Commentuser, NetInfo


class MakeShell(Rest):
    def get(self, request, *args, **kwargs):
        user = Commentuser.objects.get(username=request.session.get("username"))
        test_num = ApplyInfo.objects.filter(ins=user.ins).order_by("-acc_month")[0].test_num
        vpn_ip = NetInfo.objects.filter(ins_name=user.ins.ins_nm)[0].IP_R2C1
        with open("media/upload/apply_temp/脚本化.txt", "r") as f:
            mode = f.read()
            data1 = re.sub(r'x{10}', test_num, mode)
            data2 = re.sub(r'IP_dz', vpn_ip, data1)
            print(mode)
        with open("E:/test10.txt", "w+") as fb:
            fb.write(data2)
        response = FileResponse(data2)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=test0.txt'
        return response
