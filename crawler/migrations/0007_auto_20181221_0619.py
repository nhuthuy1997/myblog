# Generated by Django 2.1.4 on 2018-12-21 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0006_auto_20181221_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=190),
        ),
    ]