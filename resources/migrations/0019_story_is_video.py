# Generated by Django 5.0.4 on 2024-09-19 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0018_remove_story_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='is_video',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='видео?'),
        ),
    ]
