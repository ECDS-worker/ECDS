# Generated by Django 2.1.2 on 2019-01-22 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcdsApp', '0011_auto_20190122_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testfile',
            name='file_url',
            field=models.CharField(help_text='文件上传路径', max_length=128),
        ),
    ]
