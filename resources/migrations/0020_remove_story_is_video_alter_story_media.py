# Generated by Django 5.0.4 on 2024-09-19 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0019_story_is_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='is_video',
        ),
        migrations.AlterField(
            model_name='story',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='dashboard/%Y/%m/%d/', verbose_name='видео файл'),
        ),
    ]
