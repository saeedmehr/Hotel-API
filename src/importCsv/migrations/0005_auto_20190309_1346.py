# Generated by Django 2.1.7 on 2019-03-09 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importCsv', '0004_auto_20190309_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='city',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Manager',
        ),
    ]
