# Generated by Django 2.1.4 on 2018-12-19 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('N', 'New'), ('W', 'Warning'), ('R', 'Reject'), ('P', 'Publish')], default='N', max_length=1)),
                ('title', models.TextField(default='', max_length=500)),
                ('view_count', models.IntegerField(default=0)),
                ('sentences_of_summary', models.IntegerField(default=5)),
                ('summary', models.TextField(default='', max_length=2500)),
                ('hash_title', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SourceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('U', 'Unknown'), ('V', 'Viblo'), ('T', 'TechBlog'), ('I', 'ITviec'), ('J', 'JamViet')], default='U', max_length=1, unique=True)),
                ('image', models.CharField(default='', max_length=200)),
                ('description', models.TextField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('color', models.CharField(choices=[('Gray', 'default'), ('Blue', 'primary'), ('Green', 'success'), ('Light Blue', 'info'), ('Orange', 'warning'), ('Red', 'danger')], default='Gray', max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='source_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.SourceInfo'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='crawler.Tag'),
        ),
    ]
