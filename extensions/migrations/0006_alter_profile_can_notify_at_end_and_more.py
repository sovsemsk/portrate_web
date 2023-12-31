# Generated by Django 4.2.5 on 2023-11-23 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extensions', '0005_alter_profile_can_notify_at_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='can_notify_at_end',
            field=models.TimeField(blank=True, default=datetime.time(17, 0), null=True, verbose_name='можно оповещать до'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='can_notify_at_start',
            field=models.TimeField(blank=True, default=datetime.time(9, 0), null=True, verbose_name='можно оповещать с'),
        ),
    ]
