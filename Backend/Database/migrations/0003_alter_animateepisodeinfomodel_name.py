# Generated by Django 3.2.7 on 2021-10-16 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0002_auto_20211012_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animateepisodeinfomodel',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]