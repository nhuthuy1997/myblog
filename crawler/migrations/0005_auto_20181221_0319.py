# Generated by Django 2.1.4 on 2018-12-21 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0004_auto_20181221_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.CharField(default='', max_length=190),
        ),
        migrations.AlterField(
            model_name='sourceinfo',
            name='image',
            field=models.CharField(default='', max_length=190),
        ),
    ]