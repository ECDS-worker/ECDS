from api.comment import *

from api_ecds.search import MakeExcel
from api_ecds.make_shell import MakeShell
from api_ecds.excel_file import ExcelFile
from api_ecds.audit_test import Audit_Test
from api.Tec_accept import TecAccept
from api_ecds.accept_record import AcceptRecord, TestingFile
from api_ecds.check_search import CheckSearch, CheckApply


api_ecds = Register()

api_ecds.regist(MakeExcel('search'))                                 # 简略查询功能
api_ecds.regist(MakeShell('makeshell'))                              # 生成shell脚本功能
api_ecds.regist(ExcelFile('excelfile'))                              # 生成excelfile功能
api_ecds.regist(Audit_Test('audittest'))                             # 分页
api_ecds.regist(TecAccept('tecaccept'))                              # 技术接入测试
api_ecds.regist(AcceptRecord('accept_record'))                       # 接入技术验收信息表
api_ecds.regist(CheckSearch('checksearch'))                          # 验收测试搜索功能
api_ecds.regist(CheckApply('checkapply'))                            # 验收申请审核功能
api_ecds.regist(TestingFile('test_file'))                            # 检测相关技术文件
