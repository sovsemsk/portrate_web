# Generated by Django 5.0.4 on 2024-11-24 18:35

import django.db.models.deletion
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0034_rename_is_visible_profile_story_is_visible_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('is_active', models.BooleanField(default=False, verbose_name='активно?')),
                ('is_visible_yandex', models.BooleanField(default=False, verbose_name='отображать в Яндекс?')),
                ('is_visible_gis', models.BooleanField(default=False, verbose_name='отображать в 2Гис?')),
                ('is_visible_google', models.BooleanField(default=False, verbose_name='отображать в Google?')),
                ('is_visible_avito', models.BooleanField(default=False, verbose_name='отображать в Авито?')),
                ('is_visible_zoon', models.BooleanField(default=False, verbose_name='отображать в Zoon?')),
                ('is_visible_flamp', models.BooleanField(default=False, verbose_name='отображать в Flamp?')),
                ('is_visible_yell', models.BooleanField(default=False, verbose_name='отображать в Yell?')),
                ('is_visible_prodoctorov', models.BooleanField(default=False, verbose_name='отображать в Продокторов?')),
                ('is_visible_yandex_services', models.BooleanField(default=False, verbose_name='отображать в Яндекс Сервисах?')),
                ('is_visible_otzovik', models.BooleanField(default=False, verbose_name='отображать в Отзовик?')),
                ('is_visible_irecommend', models.BooleanField(default=False, verbose_name='отображать в Irecommend?')),
                ('is_visible_tripadvisor', models.BooleanField(default=False, verbose_name='отображать в Tripadvisor?')),
                ('name', models.CharField(verbose_name='название')),
                ('preview', django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', keep_meta=True, quality=75, scale=1, size=[256, 256], upload_to='dashboard/%Y/%m/%d/', verbose_name='превью')),
            ],
            options={
                'verbose_name': 'инструкция',
                'verbose_name_plural': 'инструкции',
                'db_table': 'resources_instruction',
            },
        ),
        migrations.AlterModelTable(
            name='storyslide',
            table='resources_story_slide',
        ),
        migrations.CreateModel(
            name='InstructionSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.IntegerField(default=0, verbose_name='порядок')),
                ('image', models.ImageField(blank=True, null=True, upload_to='dashboard/%Y/%m/%d/', verbose_name='изображение')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.instruction', verbose_name='история')),
            ],
            options={
                'verbose_name': 'медиа инструкции',
                'verbose_name_plural': 'медиа инструкций',
                'db_table': 'resources_instruction_slide',
            },
        ),
    ]