# Generated by Django 4.2.5 on 2023-11-18 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0011_alter_company_dikidi_rate_alter_company_flamp_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(verbose_name='дата создания'),
        ),
    ]
