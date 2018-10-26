from api.comment import *
from api.user import *
from api.filedownload import *

api = Register()
api.regist(SessionRest('session'))
api.regist(RegistCode())
api.regist(UserRest('user'))
api.regist(UploadFile('uploadfile'))
