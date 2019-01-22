from api.comment import Rest
from EcdsApp.models import ApplyInfo,NetInfo
from api.utils import json_response
from django.core.paginator import Paginator, EmptyPage


class Net(Rest):
    def get(self, request, *args, **kwargs):
        user = request.user

        data = {
            "apply_info": [],
            "page_nums": [],
        }

        try:

            all_ins = ApplyInfo.objects.filter(check_state=1)
            # 构建分页器对象,cur_apply=所有数据,2=每页显示的个数
            paginator = Paginator(all_ins, 10)
            num_page = request.GET.get("page", 1)
            page_nu = paginator.count
            data["page_nums"] = [{
                "nnn": page_nu,
            }]
            try:
                content = paginator.page(num_page)
            except EmptyPage:
                content = paginator.page(paginator.num_pages)
                for all_info in content.object_list:
                    net_infos = all_info.netinfo_set.all()
                    for net_info in net_infos:
                        print(net_info.ins_nm)

                        if all_info.ins.ins_nm == net_info.ins_nm:
                            retu_dic = dict()
                            retu_dic["id"] = all_info.id
                            retu_dic["ins_name"] = all_info.ins.ins_nm
                            retu_dic["name"] = all_info.contact_nm
                            retu_dic["phone"] = all_info.phone
                            retu_dic["email"] = all_info.email
                            retu_dic["net_ty"] = all_info.net_ty

                            retu_dic["IP_R2C1"] = net_info.IP_R2C1
                            retu_dic["system_name"] = net_info.system_name
                            retu_dic["pro_num"] = net_info.pro_num
                            retu_dic["ip"] = net_info.ip
                            retu_dic["laboratory_ip"] = net_info.laboratory_ip
                            retu_dic["server_ip"] = net_info.server_ip
                            retu_dic["pro_EquiInfo"] = net_info.pro_EquiInfo
                            data["apply_info"].append(retu_dic)
                        return json_response(data)
            else:
                for all_info in content.object_list:
                    net_infos = all_info.netinfo_set.all()
                    for net_info in net_infos:
                        if all_info.ins.ins_nm == net_info.ins_nm:
                            retu_dic = dict()
                            retu_dic["id"] = all_info.id
                            retu_dic["ins_name"] = all_info.ins.ins_nm
                            retu_dic["name"] = all_info.contact_nm
                            retu_dic["phone"] = all_info.phone
                            retu_dic["email"] = all_info.email
                            retu_dic["net_ty"] = all_info.net_ty

                            retu_dic["IP_R2C1"] = net_info.IP_R2C1
                            retu_dic["system_name"] = net_info.system_name
                            retu_dic["pro_num"] = net_info.pro_num
                            retu_dic["ip"] = net_info.ip
                            retu_dic["laboratory_ip"] = net_info.laboratory_ip
                            retu_dic["server_ip"] = net_info.server_ip
                            retu_dic["pro_EquiInfo"] = net_info.pro_EquiInfo
                            data["apply_info"].append(retu_dic)
                return json_response(data)
        except:
            pass

    def post(self, request, *args, **kwargs):

        all_news = request.POST
        # net_id = all_news.get("ins_date")
        net_all_id = all_news.get("id")
        net_ip = all_news.get("ip")
        net_server_ip = all_news.get("server_ip")
        sure_id = all_news.get("sure")

        data = {
            "ips": 200,
        }
        # if net_id == 0:
        news_all = ApplyInfo.objects.get(id=net_all_id)
        print(news_all.ins.ins_nm)
        net_info = NetInfo.objects.get(id=net_all_id)
        print(net_info.ins_nm)
        if news_all.ins.ins_nm == net_info.ins_nm:
            if sure_id == 1:
                NetInfo.objects.filter(id=net_all_id).update(IP_R2C1=net_ip, server_ip=net_server_ip)
        return json_response(data)


class IpCheck(Rest):
    pass