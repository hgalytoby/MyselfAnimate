# Generated by Django 3.2.7 on 2021-09-24 21:59

import Database.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnimateEpisodeInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('episode', models.URLField()),
                ('done', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'AnimateEpisodeInfo',
            },
        ),
        migrations.CreateModel(
            name='AnimateWebsiteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'AnimateWebsite',
            },
        ),
        migrations.CreateModel(
            name='HistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animate_website_name', models.CharField(max_length=32)),
                ('animate_name', models.CharField(max_length=128)),
                ('episode_name', models.CharField(max_length=64)),
                ('date', models.DateTimeField()),
            ],
            options={
                'db_table': 'History',
            },
        ),
        migrations.CreateModel(
            name='FinishAnimateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('url', models.URLField(unique=True)),
                ('image', models.ImageField(upload_to=Database.models.upload_path)),
                ('from_website', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Database.animatewebsitemodel')),
            ],
            options={
                'db_table': 'MyselfFinishAnimate',
            },
        ),
        migrations.CreateModel(
            name='AnimateInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('animate_type', models.CharField(blank=True, max_length=32, null=True)),
                ('premiere_date', models.CharField(blank=True, max_length=16, null=True)),
                ('episodes', models.CharField(blank=True, max_length=16, null=True)),
                ('author', models.CharField(blank=True, max_length=32, null=True)),
                ('official_website', models.URLField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=64, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=Database.models.upload_path)),
                ('synopsis', models.TextField(blank=True, null=True)),
                ('from_website', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Database.animatewebsitemodel')),
            ],
            options={
                'db_table': 'AnimateInfo',
            },
        ),
        migrations.CreateModel(
            name='AnimateEpisodeTsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_url', models.URLField()),
                ('done', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Database.animateepisodeinfomodel')),
            ],
            options={
                'db_table': 'AnimateEpisodeTs',
            },
        ),
        migrations.AddField(
            model_name='animateepisodeinfomodel',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Database.animateinfomodel'),
        ),
    ]
