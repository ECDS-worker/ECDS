# Generated by Django 2.1.2 on 2018-12-17 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EcdsApp', '0007_fornpro_mbfe_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ins_nm', models.CharField(default='', help_text='机构名称', max_length=64, null=True)),
                ('acce_ty', models.CharField(default='', help_text='接入类型', max_length=64, null=True)),
                ('dedicated', models.CharField(default='', help_text='专线情况', max_length=64, null=True)),
                ('apply_date', models.DateTimeField(auto_now_add=True, help_text='申请日期', null=True)),
                ('reply', models.CharField(default='', help_text='批复文件', max_length=64, null=True)),
                ('all_month', models.CharField(default='', help_text='是否至少测试一月', max_length=64, null=True)),
                ('acces_detec', models.CharField(default='', help_text='接入端软件测试', max_length=64, null=True)),
                ('check_time1', models.DateTimeField(blank=True, help_text='验收时间', null=True)),
                ('acces_info', models.CharField(default='', help_text='接入端信息系统检查', max_length=64, null=True)),
                ('check_time2', models.DateTimeField(blank=True, help_text='验收时间', null=True)),
                ('env_check', models.CharField(default='', help_text='接入环境检查', max_length=64, null=True)),
                ('check_time3', models.DateTimeField(blank=True, help_text='验收时间', null=True)),
                ('region', models.CharField(default='', help_text='区域', max_length=64, null=True)),
                ('city', models.CharField(default='', help_text='城市', max_length=64, null=True)),
                ('contacts', models.CharField(default='', help_text='联系人', max_length=64, null=True)),
                ('phone', models.CharField(default='', help_text='联系电话', max_length=64, null=True)),
                ('email', models.CharField(default='', help_text='邮箱', max_length=64, null=True)),
                ('computer_adr', models.CharField(default='', help_text='机房地址', max_length=64, null=True)),
                ('company_adr', models.CharField(default='', help_text='单位地址', max_length=64, null=True)),
                ('zip_code', models.CharField(default='', help_text='邮编', max_length=64, null=True)),
                ('fax', models.CharField(default='', help_text='传真', max_length=16, null=True)),
            ],
            options={
                'verbose_name': '参与者系统接入表',
                'verbose_name_plural': '参与者系统接入表',
                'db_table': 'acceptcheck',
            },
        ),
        migrations.CreateModel(
            name='SoftInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soft_nm', models.CharField(default='', help_text='软件名称', max_length=32, null=True)),
                ('soft_ty', models.CharField(default='', help_text='软件版本', max_length=16, null=True)),
                ('mid_ty', models.CharField(default='', help_text='中间件及版本', max_length=64, null=True)),
                ('database', models.CharField(default='', help_text='数据库名称及版本', max_length=32, null=True)),
                ('operat_sys', models.CharField(default='', help_text='操作系统平台及版本', max_length=64, null=True)),
                ('cd_num', models.CharField(default='', help_text='光盘数量', max_length=4, null=True)),
                ('instruct_num', models.CharField(default='', help_text='说明书数量', max_length=4, null=True)),
                ('enclosure_num', models.CharField(default='', help_text='附件数量', max_length=4, null=True)),
                ('pro_line_num', models.CharField(default='', help_text='生产环境行号', max_length=16, null=True)),
                ('pro_acc_num', models.CharField(default='', help_text='生产环境接入点号', max_length=16, null=True)),
                ('test_line_num', models.CharField(default='', help_text='测试环境行号', max_length=16, null=True)),
                ('test_acc_num', models.CharField(default='', help_text='生产环境接入点号', max_length=16, null=True)),
                ('front_info', models.CharField(default='', help_text='前置机部署情况', max_length=64, null=True)),
                ('MBFE', models.CharField(default='', help_text='MBFE版本号', max_length=8, null=True)),
                ('apply_mid', models.CharField(default='', help_text='应用部署中间件及版本', max_length=32, null=True)),
                ('message_mid', models.CharField(default='', help_text='消息中间件', max_length=32, null=True)),
                ('acces_sys', models.CharField(default='', help_text='接入系统', max_length=16, null=True)),
                ('acceptcheck', models.ForeignKey(help_text='接入测试信息表', on_delete=django.db.models.deletion.CASCADE, to='EcdsApp.AcceptCheck')),
            ],
            options={
                'verbose_name': '技术验收软件信息表',
                'verbose_name_plural': '技术验收软件信息表',
                'db_table': 'softinfo',
            },
        ),
        migrations.AlterField(
            model_name='applyinfo',
            name='check_state',
            field=models.IntegerField(blank=True, choices=[(0, '等待审核'), (1, '审核通过'), (2, '驳回'), (3, 'IP分配完成'), (4, '分配测试ccpc')], default=0, help_text='审核状态', null=True),
        ),
    ]