# Generated by Django 2.1.7 on 2019-03-10 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importCsv', '0005_auto_20190309_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url',
            field=models.URLField(),
        ),
    ]
