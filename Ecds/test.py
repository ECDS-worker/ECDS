import gzip
import tarfile
import os


def tar(fname):
    """
        压缩成.tar.gz
    """
    t = tarfile.open(fname + ".tar.gz", "w:gz")
    for root, dirs, files in os.walk(fname):
        for file_nm in files:
            fullpath = os.path.join(root, file_nm)
            t.add(fullpath)
    t.close()


def un_gz(file_name):
    """解压gz包"""
    f_name = file_name.replace(".gz", "")
    # 获取文件的名称，去掉
    g_file = gzip.GzipFile(file_name)
    # 创建gzip对象
    with open(f_name, "wb") as f:
        f.write(g_file.read())
    print(f.name)
    return f.name
    # gzip对象用read()打开后，写入open()建立的文件里。


def un_tar(file_name):
    """解压tar"""
    print(file_name)
    tar_obj = tarfile.open(file_name)
    names = tar_obj.getnames()

    if os.path.isdir(file_name + "_files"):
        print('文件已存在')
        temp_file_path = os.path.isdir(file_name + "_files")
    else:
        temp_file_path = os.mkdir(file_name + "_files")
        print('创建一个新的文件名')
    # 因为解压后是很多文件，预先建立同名目录
    for name in names:
        tar_obj.extract(name, file_name + "_files/")
    tar_obj.close()
    return temp_file_path


# 压缩包文件路径
rar_file_path = "E:\python_jb\\test_zip\\"

for dirpath, dirnames, filenames in os.walk(rar_file_path):
    # 压缩文件
    # for dirnm in dirnames:
    #     file = os.path.join(rar_file_path, dirnm)
    #     tar(file)

    for filepath in filenames:
        gz_file_path = os.path.join(dirpath, filepath)

        if gz_file_path.endswith('.tar.gz'):
            # 读取文件路径，开始进行解压操作
            gz_file = un_gz(gz_file_path)
            un_tar(gz_file)

