# Generated by Django 3.2.7 on 2021-11-05 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Database', '0005_alter_downloadmodel_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animateepisodeinfomodel',
            name='download',
        ),
        migrations.AlterField(
            model_name='downloadmodel',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='download_model', to='Database.animateepisodeinfomodel'),
        ),
    ]
