# Generated by Django 3.2.7 on 2021-11-26 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0006_auto_20211105_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historymodel',
            name='download_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]