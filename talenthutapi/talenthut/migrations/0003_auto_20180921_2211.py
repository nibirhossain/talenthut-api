# Generated by Django 2.0.5 on 2018-09-21 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talenthut', '0002_auto_20180920_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiteractivityhistory',
            name='is_unchanged',
        ),
        migrations.AddField(
            model_name='recruiteractivityhistory',
            name='is_disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recruiteractivityhistory',
            name='is_updated',
            field=models.BooleanField(default=False),
        ),
    ]