# Generated by Django 5.0.1 on 2024-01-31 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0017_company_gis_rate_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='gis_rate_stars',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='звезды 2Гис'),
        ),
    ]