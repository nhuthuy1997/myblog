# Generated by Django 2.1.4 on 2018-12-21 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='hash_name',
            field=models.BigIntegerField(default=0),
        ),
    ]