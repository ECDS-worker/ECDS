from api.comment import *
from api.user import *
from api.filedownload import *
from api.first_column import *
from api.apply_info import ApplyInfomation
from api.mk_word import MakeWord, MakeExcel
from api.search import Search

api = Register()
api.regist(Login('login'))                      # 登陆
api.regist(RegistUser('registuser'))            # 注册
api.regist(RegistCode('registcode'))            # 验证码
api.regist(UserRest('user'))                    # 用户详情
api.regist(UploadFile('uploadfile'))            # 文件上传
api.regist(Index('index'))                      # 一级栏目主页
api.regist(Notic('notice'))                     # 公告更多页面
api.regist(ApplyInfomation('applyinfomation'))  # 测试环境申请页面
api.regist(MakeWord('makeword'))                # 申请信息模板
api.regist(Search('search'))                    # 管理者搜索
api.regist(MakeExcel('excel'))                  # 生成excel表格
