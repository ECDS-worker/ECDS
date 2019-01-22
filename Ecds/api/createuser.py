import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecds.settings")
import random
import django
django.setup()

from multiprocessing import Process
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from EcdsApp.models import ApplyInfo, Insinfo
User = get_user_model()


def create_user():
    """
        批量增加用户，子表缺少很多字段使用时应该注意
    """
    for j in range(8, 50):
        ins_nm = ''
        yzm = '123456789qwertyuiopasdfghjklzxcvbnm'
        for i in range(0, 6):
            ins_nm += yzm[random.randrange(0, len(yzm))]
        ins_cd = ''
        yzm = '0123456789'
        for i in range(0, 6):
            ins_cd += yzm[random.randrange(0, len(yzm))]
        ins = Insinfo.objects.get(id=j)
        ins_tp = random.randint(0, 2)
        ins_st = random.randint(0, 2)
        check_nm = "sfkughieugrn"

        user2 = ApplyInfo.create(ins_nm, ins_cd, ins_tp, ins_st, ins, check_nm)
        user2.save()
        print(j)


# create_user()


if __name__ == "__main__":
    print('Parent process %s.' % os.getpid())
    processes = list()
    for i in range(5):
        p = Process(target=create_user)
        print('Process will start.')
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print('Process end.')
