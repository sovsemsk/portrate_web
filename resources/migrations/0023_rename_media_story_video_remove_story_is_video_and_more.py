# Generated by Django 5.0.4 on 2024-09-20 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0022_story_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='media',
            new_name='video',
        ),
        migrations.RemoveField(
            model_name='story',
            name='is_video',
        ),
        migrations.AlterField(
            model_name='story',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='dashboard/%Y/%m/%d/', verbose_name='изображение'),
        ),
    ]
