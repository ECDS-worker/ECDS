# Generated by Django 2.1.2 on 2019-01-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcdsApp', '0010_testfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tecdocuments',
            name='end_time',
            field=models.DateTimeField(help_text='失效时间'),
        ),
        migrations.AlterField(
            model_name='testfile',
            name='end_time',
            field=models.DateTimeField(help_text='失效时间'),
        ),
    ]
