# Generated by Django 5.0.1 on 2024-01-31 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0016_alter_review_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='gis_rate_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество оценок 2Гис'),
        ),
    ]