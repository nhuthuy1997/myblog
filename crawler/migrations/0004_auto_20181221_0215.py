# Generated by Django 2.1.4 on 2018-12-21 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_post_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='hash_title',
            field=models.BigIntegerField(db_index=True, default=0, unique=True),
        ),
    ]
