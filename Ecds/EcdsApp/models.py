from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# Create your models here.

CONTROL_STATE = (
    (0, "禁用"),
    (1, "启用"),
)

PRO_TS = (
    (0, "最高级"),
    (1, "第二级"),
    (2, "第三级")
)
NET_TY = (
    (0, "pc动态接入"),
    (1, "路由器防火墙")
)
MQ_TYPE = (
        ("MQ", "MQ"),
        ("TLQ", "TLQ"),
    )


class UserProfile(AbstractUser):
    """
    用户表，新型字段
    """
    GEBDER_CHOICES = (
        (0, "访问者"),
        (1, "录入员"),
        (2, "复核员"),
        (3, "发布管理员"),
        (4, "应用录入员"),
        (5, "应用管理员")
    )
    Jurisdiction = models.CharField(max_length=32, null=True, blank=True, verbose_name="权限字段")
    role = models.IntegerField(choices=GEBDER_CHOICES, default=0, verbose_name="角色信息")
    ins = models.CharField(default="", null=True, max_length=32, help_text="所属机构")

    class Meta:
        db_table = 'User'
        verbose_name = "用户"
        # 使表名在admin中显示特定的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    @classmethod
    def create(cls, password, last_login, is_superuser, username, date_joined, last_name):
        return cls(password=password, last_login=last_login, is_superuser=is_superuser, username=username,
                   date_joined=date_joined, last_name=last_name)


class Commentuser(models.Model):
    """
        一般用户信息表
    """
    GEBDER_CHOICES = (
        (0, "访问者"),
        (1, "录入员"),
        (2, "复核员"),
        (3, "发布管理员"),
        (4, "应用录入员"),
        (5, "应用管理员")
    )
    username = models.CharField(max_length=15, null=True, help_text='姓名')
    user_pw = models.CharField("用户密码", max_length=64, null=True)
    phone = models.CharField(default='', max_length=16, null=True, help_text="手机号码")
    email = models.EmailField(default='', blank=True, null=True, help_text='邮箱')
    mk_time = models.DateField(auto_now_add=True, null=True, blank=True, help_text="创建日期")
    last_login = models.DateField(auto_now=True, null=True, blank=True,  help_text="最后登陆时间")
    activate = models.IntegerField(default=0, help_text="用户状态")
    Jurisdiction = models.CharField(max_length=32, null=True, verbose_name="权限字段")
    role = models.IntegerField(choices=GEBDER_CHOICES, default=0, verbose_name="角色信息")
    ins = models.ForeignKey('Insinfo', help_text="关联机构表", on_delete=models.CASCADE)

    class Meta:
        db_table = 'Commentuser'
        verbose_name = '客户信息表'
        verbose_name_plural = verbose_name


class Insinfo(models.Model):
    """
        机构信息表，包含前置信息表的内容
    """
    ins_nm = models.CharField(max_length=64, null=False, help_text="机构名称")
    ins_cd = models.CharField(max_length=16, null=False, help_text="机构号")
    sum_num = models.CharField(default="", max_length=16, null=True, help_text="总行行号")
    pay_num = models.CharField(default="", max_length=16, null=True, help_text="支付系统行号")
    vip_code = models.CharField(default="", max_length=16, null=True, help_text="会员代码")
    ins_tp = models.CharField(default="", max_length=4, null=False, help_text="机构类型")
    ins_st = models.IntegerField(default=0, choices=CONTROL_STATE, help_text="机构状态")
    ins_location = models.CharField(default='', max_length=16, null=True, help_text="机构所在地")
    ins_sysytem = models.CharField(default='', max_length=16, null=True, help_text="机构所属系统")
    access_port = models.CharField(default="", max_length=16, null=True, help_text="接入点号")
    port = models.CharField(default='', max_length=8, null=True, help_text="端口")
    mid = models.CharField(default="MQ", max_length=32, choices=MQ_TYPE, help_text="中间件类型")

    class Meta:
        db_table = 'insinfo'
        verbose_name = '客户信息表'
        verbose_name_plural = verbose_name

    @classmethod
    def create(cls, ins_nm, ins_cd, ins_tp, ins_st):
        return cls(ins_nm=ins_nm, ins_cd=ins_cd, ins_tp=ins_tp, ins_st=ins_st)


class UserForm(models.Model):
    """
        上传文件记录表
    """
    # user = models.ForeignKey("Commentuser", on_delete=models.CASCADE, help_text='用户名')
    username = models.CharField(default="", max_length=16, null=True, help_text="用户名")
    ins_nm = models.CharField(default="", max_length=64, null=True, help_text="所属机构名称")
    file_url = models.CharField(max_length=128, null=False, help_text='存储路径')
    filename = models.CharField(max_length=32, null=False, help_text='文件名称')
    up_time = models.DateTimeField(auto_now=True, null=False, help_text='上传时间')
    bank_num = models.CharField(max_length=36, null=False, help_text="行号")
    empty = models.CharField(max_length=20, null=False, help_text="预留字段")

    class Meta:
        db_table = 'UserForm'
        verbose_name = '上传信息表'
        verbose_name_plural = verbose_name

    @classmethod
    def create(cls, username, ins_nm, fileurl, filename,):
        return cls(username=username, ins_nm=ins_nm, file_url=fileurl, filename=filename)


class ApplyInfo(models.Model):
    """
        机构申请信息表
        缺少一个接入ECDS方式
    """
    CHECK_STA = (
        (0, "等待审核"),
        (1, "审核通过"),
        (2, "驳回"),
        (3, "IP分配完成"),
        (4, "分配测试ccpc")
    )

    ACC_TY = (
        (0, "直连"),
        (1, "客户端")
    )

    ins = models.ForeignKey('Insinfo', help_text="所属机构表", on_delete=models.CASCADE)
    contact_nm = models.CharField(default="", max_length=16, null=True, help_text="联系人名字")
    bank_num = models.CharField(max_length=32, null=False, help_text="行号")
    production_ccpc = models.CharField(default="", max_length=32, null=False, help_text="生产CCPC")
    test_ccpc = models.CharField(default="", max_length=48, null=True, help_text="测试CCPC")
    test_num = models.CharField(default="", max_length=48, null=True, help_text="测试环境接入点号")
    product_num = models.CharField(default="", max_length=48, null=True, help_text="生产环境接入点号")
    phone = models.CharField(default='', max_length=16, blank=True, null=True, help_text="手机号码")
    email = models.EmailField(default='', blank=True, null=True, help_text='邮箱')
    soft_nm = models.CharField(default="", max_length=16, null=True, help_text="内部软件名称")
    soft_type = models.CharField(default="", max_length=32, null=True, help_text="内部系统软件版本")
    mid_message = models.CharField(default="MQ", max_length=32, choices=MQ_TYPE, help_text="消息中间件类型")
    mid_apply = models.CharField(default="MQ", max_length=32, choices=MQ_TYPE, help_text="应用件类型")
    start_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="开始时间")
    end_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="结束时间")
    first_access = models.IntegerField(default=1, null=True, blank=True, help_text="是否首次接入")
    net_ty = models.IntegerField(default=0, choices=NET_TY, null=True, blank=True, help_text="网络接入方式")
    acc_ecds = models.CharField(default=0, max_length=16, null=True, help_text="网络接入方式")
    access_obj = models.TextField(default='', help_text="接入目的")
    check_state = models.IntegerField(default=0, choices=CHECK_STA, null=True, blank=True, help_text="审核状态")
    check_nm = models.CharField(default="", max_length=20, null=False, help_text="审核人")
    support_name = models.CharField(default="", max_length=16, null=True, help_text="ECDS支持人员信息")
    acc_month = models.CharField(default="", max_length=20, null=False, help_text="加入月份")

    class Meta:
        db_table = "ApplyInfo"
        verbose_name = "机构申请信息表"
        verbose_name_plural = verbose_name

    @classmethod
    def create(cls, ins_nm, ins_cd, ins_tp, ins_st, ins, check_nm):
        return cls(contact_nm=ins_nm, bank_num=ins_cd, production_ccpc=ins_tp, test_num=ins_st, ins=ins,
                   check_nm=check_nm)


class Notice(models.Model):
    """
        公告表
    """
    notice_nm = models.CharField(default='', max_length=128, null=True, help_text="公告名称")
    notice_cont = models.TextField(default='', max_length=256, null=True, help_text="公告内容")
    publisher = models.CharField(default='', max_length=16, null=True, help_text="发布人")
    activate = models.IntegerField(default=0, choices=CONTROL_STATE, help_text="活跃状态")
    start_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="创建时间")
    end_time = models.DateTimeField(null=True, blank=True, help_text="失效时间")
    priority = models.IntegerField(default=9, null=True, blank=True, help_text="优先级")

    class Meta:
        db_table = "Notice"
        verbose_name = "公告表"
        verbose_name_plural = verbose_name
        ordering = ["priority"]


class TecDocuments(models.Model):
    """
        技术文件, 机构关联可取消
    """
    username = models.CharField(default="", max_length=16, null=True, help_text='上传人')
    file_url = models.CharField(max_length=512, null=False, help_text='存储路径')
    filename = models.CharField(max_length=32, null=False, help_text='文件名称')
    up_time = models.DateTimeField(auto_now=True, null=False, help_text='上传时间')
    activate = models.IntegerField(default=0, choices=CONTROL_STATE, help_text="活跃状态")
    end_time = models.DateTimeField(auto_now=False, null=False, blank=False, help_text="失效时间")
    priority = models.IntegerField(default=9, null=True, blank=True, help_text="优先级")

    class Meta:
        db_table = "TecDocuments"
        verbose_name = "技术文件"
        verbose_name_plural = verbose_name
        ordering = ["priority"]


class ContactsInfo(models.Model):
    """
        联系人信息表
    """
    ROLE_TY = (
        ("系统接口人", "系统接口人"),
        ("网络接口人", "网络接口人"),
        ("业务人员", "业务人员"),
        ("技术人员", "技术人员")
    )
    name = models.CharField(default='', max_length=16, null=False, help_text="联系人姓名")
    role = models.CharField(default="技术人员", max_length=8, choices=ROLE_TY, help_text="角色")
    phone = models.CharField(max_length=16, null=False, help_text="联系方式")
    email = models.CharField(max_length=16, null=False, help_text="邮箱")
    ins = models.ForeignKey("Insinfo", help_text="所属机构表", on_delete=models.CASCADE)
    priority = models.IntegerField(default=9, null=True, blank=True, help_text="优先级")
    contactuser = models.ForeignKey("NetInfo", help_text="运维联系人信息", on_delete=models.CASCADE)

    class Meta:
        db_table = "ContactsInfo"
        verbose_name = "联系人信息表"
        verbose_name_plural = verbose_name
        ordering = ["priority"]


class LogInfo(models.Model):
    """
        操作日志表
    """
    username = models.CharField(max_length=16, null=True, help_text="用户名")
    ins = models.CharField(max_length=32, null=True, help_text="所属机构名称")
    operation = models.TextField(default='', null=True, help_text="操作内容")
    nm_id = models.CharField(max_length=20, null=False, help_text="用户ID")

    class Meta:
        db_table = "LogInfo"
        verbose_name = "操作日志表"
        verbose_name_plural = verbose_name


class LoginRecord(models.Model):
    """
    登陆日志表
    """
    user_id = models.CharField(max_length=20, null=False, help_text="用户id")
    user_name = models.CharField(max_length=20, null=False, help_text="用户名")
    user_ip = models.CharField(max_length=32, null=False, help_text="用户IP")
    bank_name = models.CharField(max_length=32, null=False, help_text="行名")
    bank_num = models.CharField(max_length=32, null=False, help_text="行号")
    login_time = models.DateTimeField(null=False, help_text="登陆时间")
    empty = models.CharField(max_length=20, null=True, help_text="预留字段")

    class Meta:
        db_table = "LoginRecord"
        verbose_name = "登陆日志表"
        verbose_name_plural = verbose_name


class TimeMax(models.Model):
    """
        工作时间和每月最大值
    """
    username = models.CharField(default="", max_length=16, null=True, help_text="发布用户名")
    start_time = models.DateField(null=True, help_text="当月工作日开始时间")
    end_time = models.DateField(null=True, help_text="当月工作日结束时间")
    max_acc = models.IntegerField(null=True, blank=True, help_text="当月最大接入数")
    author_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="发布时间")
    empty = models.CharField(max_length=20, null=True, help_text="预留字段")

    class Meta:
        db_table = "TimeMax"
        verbose_name = "限制表"
        verbose_name_plural = verbose_name


class FornPro(models.Model):
    """
    前置机信息表
    """
    aply_info = models.ForeignKey("ApplyInfo", help_text="机构信息表", on_delete=models.CASCADE)
    bank_num = models.CharField(default="", max_length=64, help_text="支付系统行号")
    ins_nm = models.CharField(default="", max_length=64, help_text="机构名称")
    mbfe_type = models.CharField(default="", max_length=64, help_text="MBFE版本")
    mid_type = models.CharField(default="", max_length=64, help_text="中间件类型")
    port = models.CharField(default="", max_length=64, help_text="队列消息管理器")
    join_num = models.CharField(default="", max_length=64, help_text="接入点号")
    pro_version = models.CharField(max_length=128, null=True, help_text="前置机版本")
    pro_system = models.CharField(max_length=128, null=True, help_text="前置机操作系统")

    class Meta:
        db_table = "fornpro"
        verbose_name = "前置机信息表"
        verbose_name_plural = verbose_name


class NetInfo(models.Model):
    """
    网络配置信息表
    IP_R2C1和ip字段需要交换位置
    """
    aply_info = models.ForeignKey("ApplyInfo", help_text="机构信息表", on_delete=models.CASCADE)
    ins_nm = models.CharField(default="", max_length=64, help_text="机构名称")
    net_ty = models.IntegerField(default=0, choices=NET_TY, null=True, blank=True, help_text="vpn网络接入方式")
    ip = models.CharField(max_length=32, null=True, help_text="参与者 VPN接入设备公网地址")
    system_name = models.CharField(max_length=32, null=True, help_text="接入业务系统名称")
    pro_num = models.CharField(max_length=32, null=True, help_text="业务前置机数量")
    IP_R2C1 = models.CharField(max_length=32, null=True, help_text="参与者外联通信IP地址")
    laboratory_ip = models.CharField(max_length=32, null=True, help_text="VPN接入实验室测试环境设备公网地址")
    server_ip = models.CharField(max_length=32, null=True, help_text="系统接入测试实验室服务器外部通信地址段")
    pro_EquiInfo = models.CharField(max_length=48, null=True, help_text="参与者VPN接入设备信息（品牌、型号）")

    class Meta:
        db_table = "NetInfo"
        verbose_name = "前置机信息表"
        verbose_name_plural = verbose_name


class AcceptCheck(models.Model):
    """
        接入验收信息统计表
        缺少审核状态
    """
    CHECK_STA = (
        (0, "待审核"),
        (1, "审核通过"),
        (2, "驳回")
    )
    ins_nm = models.CharField(default="", max_length=64, null=True, help_text="机构名称")
    acce_ty = models.CharField(default="", max_length=64, null=True, help_text="接入类型")
    dedicated = models.CharField(default="", max_length=64, null=True, help_text="专线情况")
    apply_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="申请日期")
    reply = models.CharField(default="", max_length=64, null=True, help_text="批复文件")
    all_month = models.CharField(default="", max_length=64, null=True, help_text="是否至少测试一月")
    acces_detec = models.CharField(default="", max_length=64, null=True, help_text="接入端软件测试")
    check_time1 = models.DateTimeField(null=True, blank=True, help_text="验收时间")
    acces_info = models.CharField(default="", max_length=64, null=True, help_text="接入端信息系统检查")
    check_time2 = models.DateTimeField(blank=True, null=True, help_text="验收时间")
    env_check = models.CharField(default="", max_length=64, null=True, help_text="接入环境检查")
    check_time3 = models.DateTimeField(blank=True, null=True, help_text="验收时间")
    region = models.CharField(default="", max_length=64, null=True, help_text="区域")
    city = models.CharField(default="", max_length=64, null=True, help_text="城市")
    contacts = models.CharField(default="", max_length=64, null=True, help_text="联系人")
    phone = models.CharField(default="", max_length=64, null=True, help_text="联系电话")
    email = models.CharField(default="", max_length=64, null=True, help_text="邮箱")
    computer_adr = models.CharField(default="", max_length=64, null=True, help_text="机房地址")

    company_adr = models.CharField(default="", max_length=64, null=True, help_text="单位地址")
    zip_code = models.CharField(default="", max_length=64, null=True, help_text="邮编")
    fax = models.CharField(default="", max_length=16, null=True, help_text="传真")
    check_state = models.IntegerField(default=0, choices=CHECK_STA, help_text="审核状态")
    Spare = models.CharField(default="", max_length=16, null=True, help_text="备用字段")

    class Meta:
        db_table = "acceptcheck"
        verbose_name = "参与者系统接入表"
        verbose_name_plural = verbose_name


class SoftInfo(models.Model):
    """
        技术验收软件信息表
        空白处可以添加外键进行关联
    """
    acceptcheck = models.ForeignKey("AcceptCheck", on_delete=models.CASCADE, help_text="接入测试信息表")
    soft_nm = models.CharField(default="", max_length=32, null=True, help_text="软件名称")
    soft_ty = models.CharField(default="", max_length=16, null=True, help_text="软件版本")
    mid_ty = models.CharField(default="", max_length=64, null=True, help_text="中间件及版本")
    database = models.CharField(default="", max_length=32, null=True, help_text="数据库名称及版本")
    operat_sys = models.CharField(default="", max_length=64, null=True, help_text="操作系统平台及版本")
    cd_num = models.CharField(default="", max_length=4, null=True, help_text="光盘数量")
    instruct_num = models.CharField(default="", max_length=4, null=True, help_text="说明书数量")
    enclosure_num = models.CharField(default="", max_length=4, null=True, help_text="附件数量")
    # pro_line_num = models.CharField(default="", max_length=16, null=True, help_text="生产环境行号")
    # pro_acc_num = models.CharField(default="", max_length=16, null=True, help_text="生产环境接入点号")
    # test_line_num = models.CharField(default="", max_length=16, null=True, help_text="测试环境行号")
    # test_acc_num = models.CharField(default="", max_length=16, null=True, help_text="生产环境接入点号")
    # front_info = models.CharField(default="", max_length=64, null=True, help_text="前置机部署情况")
    # MBFE = models.CharField(default="", max_length=8, null=True, help_text="MBFE版本号")
    # apply_mid = models.CharField(default="", max_length=32, null=True, help_text="应用部署中间件及版本")
    # message_mid = models.CharField(default="", max_length=32, null=True, help_text="消息中间件")
    test_descrip = models.TextField(max_length=512, help_text="测试说明")
    acces_sys = models.CharField(default="", max_length=16, null=True, help_text="接入系统")
    acces_type = models.CharField(default="", max_length=16, null=True, help_text="接入方式")
    Spare = models.CharField(default="", max_length=16, null=True, help_text="备用字段")

    class Meta:
        db_table = "softinfo"
        verbose_name = "技术验收软件信息表"
        verbose_name_plural = verbose_name


class TestFile(models.Model):
    """
        检测技术文档  待用
    """
    up_user = models.CharField(max_length=32, null=False, help_text="上传人")
    up_date = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="上传时间")
    file_nm = models.CharField(max_length=64, null=False, help_text="上传文件名称")
    file_url = models.CharField(max_length=128, null=False, help_text="文件上传路径")
    check_status = models.IntegerField(default=0, choices=CONTROL_STATE, help_text="审核状态")
    end_time = models.DateTimeField(auto_now=False, null=False, blank=False, help_text="失效时间")
    priority = models.IntegerField(default=9, null=True, blank=True, help_text="优先级")
    spare = models.CharField(default="", max_length=16, null=True, help_text="备用字段")

    class Meta:
        db_table = "testfile"
        verbose_name = "检测技术文档"
        verbose_name_plural = verbose_name
