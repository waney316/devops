# Generated by Django 3.2 on 2021-08-28 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auditlogmodel',
            old_name='uri',
            new_name='url',
        ),
        migrations.AlterModelTable(
            name='auditlogmodel',
            table='audit_login_log',
        ),
    ]