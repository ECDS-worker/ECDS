from api.comment import *
from EcdsApp.models import *
from api.utils import json_response
from django.db.models import Q
from django.core.paginator import Paginator


class AuditTest(Rest):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            cur_apply = ApplyInfo.objects.filter(check_state=0)
            data = {
                "apply_info": []
            }
            # 从前端获取当前的页码数,默认为1
            page_num = int(request.GET.get('page', 1))
            p = Paginator(cur_apply, 3)
            page = p.page(page_num).object_list
            for all_ins in page:
                new_dic = dict()
                new_dic["username"] = user.username
                new_dic["role"] = user.role
                new_dic["iemail"] = user.email
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
                new_dic["pro_version"] = all_ins.pro_version
                new_dic["pro_system"] = all_ins.pro_system
                new_dic["first_access"] = all_ins.first_access
                new_dic["access_ty"] = all_ins.access_ty
                new_dic["net_tynet_ty"] = all_ins.net_ty
                new_dic["access_obj"] = all_ins.access_obj
                data["apply_info"].append(new_dic)
            return json_response(data)

        except Exception as e:
            return json_response({"msg": str(e)})

    def post(self, request, *args, **kwargs):
        news_check = request.POST
        data = {
            "statu": "200"
        }
        check_state = news_check.get("check_state")
        info_id = news_check.get("id")

        ApplyInfo.objects.filter(id=info_id).update(check_state=check_state)

        return json_response(data)
