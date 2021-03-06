# Generated by Django 3.2 on 2021-08-28 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(db_index=True, help_text='uri', max_length=254, verbose_name='URI')),
                ('method', models.CharField(db_index=True, help_text='请求方式', max_length=20, verbose_name='请求方式')),
                ('query_string', models.CharField(help_text='URL请求参数', max_length=254, null=True, verbose_name='URL请求参数')),
                ('body', models.TextField(help_text='请求Body数据', verbose_name='请求Body数据')),
                ('remote_ip', models.CharField(help_text='远程主机IP', max_length=50, verbose_name='远程主机IP')),
                ('username', models.CharField(help_text='请求用户', max_length=50, verbose_name='请求用户')),
                ('status_code', models.IntegerField(blank=True, help_text='请求状态码', null=True, verbose_name='请求状态码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'API 审计',
                'verbose_name_plural': 'API 审计',
                'db_table': 'audit_log',
                'ordering': ['-create_time'],
            },
        ),
    ]
