from api.comment import Rest
from EcdsApp.models import *
from api.utils import json_response
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
import smtplib
from email.mime.text import MIMEText
from api.decorators import ecdsuser_release


class Audit_Test(Rest):
    @ecdsuser_release
    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            "page_per": [],
            "apply_info": [],
            "user": [],
        }
        error = {
            "error": "请求数据不存在"
        }
        try:
            cur_apply = ApplyInfo.objects.all().exclude(Q(check_state=1) | Q(check_state=2))
            # 构建分页器对象,cur_apply=所有数据,3=每页显示的个数
            paginator = Paginator(cur_apply, 10)
            num_page = request.GET.get("page", 1)
            page_nums = paginator.count
            data["user"] = [{
                "username": user.username,
                "role": user.role,
                "eamil": user.email,
            }]
            data["page_per"] = [{
                "page_nums": page_nums,
            }]
            try:
                content = paginator.page(num_page)
            except EmptyPage:
                return json_response(error)
            else:
                for all_ins in content.object_list:
                    print(all_ins)
                    new_dic = dict()
                    new_dic["id"] = all_ins.id
                    new_dic["ins_name"] = all_ins.ins.ins_nm
                    new_dic["ins_cd"] = all_ins.ins.ins_cd
                    new_dic["port"] = all_ins.ins.port
                    new_dic["access_port"] = all_ins.ins.access_port
                    new_dic["phone"] = all_ins.phone
                    new_dic["email"] = all_ins.email
                    new_dic["bank_num"] = all_ins.bank_num
                    new_dic["test_num"] = all_ins.test_num
                    new_dic["production_ccpc"] = all_ins.production_ccpc
                    new_dic["start_time"] = all_ins.start_time.strftime("%Y-%m-%d")
                    new_dic["end_time"] = all_ins.end_time.strftime("%Y-%m-%d")
                    new_dic["soft_nm"] = all_ins.soft_nm
                    new_dic["mid_message"] = all_ins.mid_message
                    new_dic["mid_apply"] = all_ins.mid_apply
                    new_dic["first_access"] = all_ins.first_access
                    new_dic["net_ty"] = all_ins.net_ty
                    new_dic["access_obj"] = all_ins.access_obj
                    data["apply_info"].append(new_dic)
        except Exception as e:
            print(e)
            # return json_response({"msg": str(e)})
        return json_response(data)

    @ecdsuser_release
    def post(self, request, *args, **kwargs):
        news_check = request.POST
        data = {
            "statu": "200"
        }
        check_state = news_check.get("check_state")
        info_id = news_check.get("id")

        ApplyInfo.objects.filter(id=info_id).update(check_state=check_state)
        if ApplyInfo.objects.get(id=info_id).check_state == 1:
            # 邮箱服务器地址
            mailserver = "smtp.163.com"

            username_sender = "linyi3537@163.com"
            password = "311219ma"
            username_recv = "844364398@qq.com"
            mail = MIMEText("您所提交的测试申请以审核，请注意查看官网动态")
            mail["Subject"] = "上海票据交易所回复邮件"
            mail["From"] = username_sender  # 发件人
            mail["To"] = username_recv
            smtp = smtplib.SMTP(mailserver, port=25)
            smtp.login(username_sender, password)  # 登录邮箱
            smtp.sendmail(username_sender, username_recv, mail.as_string())  # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
            smtp.quit()  # 发送完毕后退出smtp
            print('success')
        return json_response(data)

    @ecdsuser_release
    def put(self, request, *args, **kwargs):
        """
            预览用户上传pdf文件, 筛选条件为行号 不是机构名称
        """
        # user = request.user
        data = request.PUT
        info_id = data.get("id")
        try:
            ins = ApplyInfo.objects.get(id=info_id).ins
            file_url = UserForm.objects.get(bank_num=ins.pay_num).file_url.split("/", 4)[-1]
        except Exception as e:
            return json_response({"msg": str(e)})
        return json_response({"url": file_url})
