from _datetime import datetime

from api.utils import json_response
from EcdsApp.models import ApplyInfo, Insinfo, ContactsInfo, Commentuser, NetInfo, FornPro
from api.comment import Rest
from django.contrib.auth import get_user_model
from api.decorators import commentuser_required

User = get_user_model()


class ApplyInfomation(Rest):
    @commentuser_required
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.username:
            username = request.session.get("username")
            user = Commentuser.objects.get(username=username)
        data = {
            "username": user.username,
            "apply_info": [],
            "ins": [],
            "user": []
        }
        try:
            ins = Insinfo.objects.get(ins_nm=user.ins.ins_nm)
            cur_apply = ApplyInfo.objects.get(ins=ins)
            forn = FornPro.objects.get(ins_nm=ins.ins_nm)
        except Exception as e:
            data["msg"] = e
            return json_response(data)
        else:
            data["ins"] = [
                {
                    "ins_nm": ins.ins_nm,
                    "ins_cd": ins.ins_cd,
                    "port": ins.port,

                    "pay_num": ins.pay_num,
                    "vip_code": ins.vip_code,

                    "access_port": ins.access_port
                }
            ]
            data["apply_info"] = [{
                "contact_nm": cur_apply.contact_nm,
                "phone": cur_apply.phone,
                "email": cur_apply.email,
                "bank_num": cur_apply.bank_num,
                "test_num": cur_apply.test_num,
                "production_ccpc": cur_apply.production_ccpc,
                "start_time": cur_apply.start_time.strftime("%Y-%m-%d"),
                "end_time": cur_apply.end_time.strftime("%Y-%m-%d"),
                "soft_nm": cur_apply.soft_nm,
                "soft_type": cur_apply.soft_type,
                "mid_message": cur_apply.mid_message,
                "mid_apply": cur_apply.mid_apply,
                "pro_version": forn.pro_version,
                "pro_system": forn.pro_system,

                "mbfe_type": forn.mbfe_type,

                "first_access": cur_apply.first_access,
                "access_ty": cur_apply.access_ty,
                "net_ty": cur_apply.net_ty,
                "access_obj": cur_apply.access_obj,
                "username": cur_apply.contact_nm,
                # "username": cur_apply.contact_nm,
            }]

        user_info = ContactsInfo.objects.filter(ins=ins)

        if user_info:
            for per_user in user_info:
                dic = dict()
                dic["username"] = per_user.name
                dic["role"] = per_user.role
                dic["phone"] = per_user.phone
                dic["email"] = per_user.email
                data["user"].append(dic)
        return json_response(data)

    @commentuser_required
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.username:
            username = request.session.get("username")
            user = Commentuser.objects.get(username=username)
        ins_nm = user.ins.ins_nm

        retu_data = {
            "status": "0",
            "msg": ""
        }
        data = request.POST
        try:
            ins = Insinfo.objects.get(ins_nm=ins_nm)  # 前提是机构表提前存在，不然这里需要改动
        except Exception as e:
            retu_data["status"] = "0"
            retu_data["msg"] = e
            return json_response(retu_data)
        now_time = datetime.now().strftime("%m")
        ApplyInfo.objects.get_or_create(ins=ins, acc_month=now_time)
        NetInfo.objects.get_or_create(ins_nm=ins.ins_nm)

        catalog_id = int(data.get("id"))
        if catalog_id == 1:                                     # 机构基础信息
            ins_name = data.get('ins_nm')
            bank_num = data.get('bank_num')
            pay_num = data.get('pay_num')
            vip_code = data.get('vip_code')
            test_num = data.get('test_num')
            production_ccpc = data.get('production_ccpc')
            if ins_name != ins_nm:
                retu_data["status"] = "0"
                retu_data["msg"] = "机构名称输入错误"
                return json_response(retu_data)
            ApplyInfo.objects.filter(ins=ins, acc_month=now_time).update(bank_num=bank_num, test_num=test_num,
                                                                         production_ccpc=production_ccpc)
            Insinfo.objects.filter(ins_nm=ins_nm).update(pay_num=pay_num, vip_code=vip_code)
            retu_data["status"] = "200"
        elif catalog_id == 2:                                   # 系统选择
            system = data.get('system')
            ApplyInfo.objects.filter(ins=ins, acc_month=now_time).update(operating=system)
            retu_data["status"] = "200"
        elif catalog_id == 3:                                   # 申请时间
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            ApplyInfo.objects.filter(ins=ins, acc_month=now_time).update(start_time=start_time, end_time=end_time)
            retu_data["status"] = "200"
        elif catalog_id == 4:                                   # 接口软件信息
            soft_nm = data.get('soft_nm')
            soft_ty = data.get('soft_type')
            mid_message = data.get('mid_message')
            mid_apply = data.get('mid_apply')
            mbfe_type = data.get('mbfe_type')
            pro_version = data.get('pro_version')
            pro_system = data.get('pro_system')
            ApplyInfo.objects.filter(ins=ins, acc_month=now_time).update(soft_nm=soft_nm, soft_type=soft_ty,
                                                                         mid_message=mid_message, mid_apply=mid_apply)
            FornPro.objects.filter(ins_nm=ins_nm).update(mbfe_type=mbfe_type, pro_version=pro_version,
                                                         pro_system=pro_system)
            retu_data["status"] = "200"
        elif catalog_id == 5:                                   # 网络接入方式
            net_ty = int(data.get('net_ty'))
            first_access = int(data.get('first_access'))
            ApplyInfo.objects.filter(ins=ins, acc_month=now_time).update(net_ty=net_ty, first_access=first_access)
            retu_data["status"] = "200"
        elif catalog_id == 6:                                   # 测试环境接入目的
            access_obj = data.get('access_obj')
            ApplyInfo.objects.filter(ins=ins, acc_month=now_time).update(access_obj=access_obj)
            retu_data["status"] = "200"
        elif catalog_id == 7:                                   # 前置机信息
            ins_cd = data.get('ins_cd')
            port = data.get('port')
            access_port = data.get('access_port')
            Insinfo.objects.filter(ins_nm=ins_nm, acc_month=now_time).update(ins_cd=ins_cd, port=port,
                                                                             access_port=access_port)
            retu_data["status"] = "200"
        elif catalog_id == 8:                                                   # 联系人信息
            contact_nm = data.get('contact')
            phone = data.get('phone')
            email = data.get('email')
            ApplyInfo.objects.filter(ins=ins, acc_month=now_time).update(contact_nm=contact_nm, phone=phone, email=email)
            retu_data["status"] = "200"
        else:
            net_ty = data.get('net_ty')
            laboratory_ip = data.get('laboratory_ip')
            system_name = data.get('system_name')
            pro_num = data.get('pro_num')
            pro_equiinfo = data.get('pro_EquiInfo')
            ApplyInfo.objects.filter(ins=ins, acc_month=now_time).update(net_ty=net_ty)
            NetInfo.objects.filter(ins_nm=ins.ins_nm).update(laboratory_ip=laboratory_ip, system_name=system_name,
                                                             pro_num=pro_num, pro_EquiInfo=pro_equiinfo)
        return json_response(retu_data)
