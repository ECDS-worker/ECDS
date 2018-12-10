from api.utils import *
from api.comment import Rest
from EcdsApp.models import Notice, TecDocuments, Commentuser


class Index(Rest):
    """
        主页内容显示
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.username:
            username = request.session.get("username")
            user = Commentuser.objects.get(username=username)
        data = {
            "username": user.username
        }
        try:
            # 主页公告栏
            notic = Notice.objects.filter(activate=1).order_by('start_time')
            per_notic = []
            file_id = 0
            for note in notic:
                objs = dict()
                objs["id"] = file_id
                objs["title"] = note.notice_nm
                objs['time'] = note.start_time.strftime('%Y-%m-%d')
                per_notic.append(objs)
                file_id += 1
        except Exception as e:
            return json_response({"msg": str(e)})
        else:
            data["notic"] = per_notic

        try:
            # 主页技术文件支持
            index_file = [tec.filename for tec in TecDocuments.objects.filter(activate=1).order_by("up_time")]
            per_ind = []
            file_id = 0
            for ind in index_file:
                objs = dict()
                objs["id"] = file_id
                objs["title"] = ind
                per_ind.append(objs)
                file_id += 1
        except Exception as e:
            return json_response({"msg": str(e)})
        else:
            data["index_file"] = per_ind

        return json_response(data)

    def post(self, request, *args, **kwargs):
        """
        公告详情页
        :param args: filename
        """
        data = request.POST
        file_id = data.get('id', '')
        try:
            notic_content = Notice.objects.filter(activate=1).order_by('start_time')[file_id].notice_cont
        except Exception as e:
            return json_response({"msg": str(e)})
        return json_response({"content": notic_content})


class Notic(Rest):
    """
        显示全部公告内容
    """
    def get(self, request, *args, **kwargs):
        data = {
            "title": ""
        }
        try:
            content = [noti.notice_nm for noti in Notice.objects.all().order_by('start_time')]
            per_ind = []
            for ind in content:
                objs = dict()
                objs["title"] = ind
                per_ind.append(objs)
            data["title"] = per_ind
        except Exception as e:
            return json_response({"msg": str(e)})
        return json_response(data)
