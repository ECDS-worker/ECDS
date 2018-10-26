import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecds.settings")
import random
import django
django.setup()

from multiprocessing import Process

from EcdsApp.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()


def create_user():
    """
        批量增加用户，子表缺少很多字段使用时应该注意
    """
    for j in range(0, 71):
        passwd = ''
        yzm = '123456789qwertyuiopasdfghjklzxcvbnm'
        for i in range(0, 6):
            passwd += yzm[random.randrange(0, len(yzm))]

        passwd_hash = make_password(passwd)

        last_login = '2018-10-10 16:39:51.830445'
        date_joined = '2018-10-10 16:39:51.830445'

        username = ''
        yzm = '123456789qwertyuiopasdfghjklzxcvbnm'
        for i in range(0, 6):
            username += yzm[random.randrange(0, len(yzm))]

        user = User.create(passwd_hash, last_login, 0, username, date_joined, passwd)
        user.save()
        user2 = UserInfo.create(user=User.objects.get(username=username))
        user2.save()
        print(j)


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
