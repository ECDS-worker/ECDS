from api.comment import *

from api_ecds.search import MakeExcel
from api_ecds.make_shell import MakeShell
from api_ecds.excel_file import ExcelFile
from api_ecds.audit_test import AuditTest


api_ecds = Register()

api_ecds.regist(MakeExcel('search'))                                 # 简略查询功能
api_ecds.regist(MakeShell('makeshell'))                              # 生成shell脚本功能
api_ecds.regist(ExcelFile('excelfile'))                              # 生成excelfile功能
api_ecds.regist(AuditTest('audittest'))                             # 分页

