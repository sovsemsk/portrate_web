# Generated by Django 4.2.5 on 2023-11-18 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0010_rename_yandex_stars_company_yandex_rate_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='dikidi_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Dikidi'),
        ),
        migrations.AlterField(
            model_name='company',
            name='flamp_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Flamp'),
        ),
        migrations.AlterField(
            model_name='company',
            name='gis_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг 2Гис'),
        ),
        migrations.AlterField(
            model_name='company',
            name='google_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Google'),
        ),
        migrations.AlterField(
            model_name='company',
            name='irecommend_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Irecommend'),
        ),
        migrations.AlterField(
            model_name='company',
            name='mapsme_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Mapsme'),
        ),
        migrations.AlterField(
            model_name='company',
            name='otzovik_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Отзовик'),
        ),
        migrations.AlterField(
            model_name='company',
            name='portrate_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Портрет'),
        ),
        migrations.AlterField(
            model_name='company',
            name='prodoctorov_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Продокторов'),
        ),
        migrations.AlterField(
            model_name='company',
            name='restoclub_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Рестоклуб'),
        ),
        migrations.AlterField(
            model_name='company',
            name='tripadvisor_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Tripadvisor'),
        ),
        migrations.AlterField(
            model_name='company',
            name='yandex_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Яндекс'),
        ),
        migrations.AlterField(
            model_name='company',
            name='yandex_rate_stars',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='звезды Яндекс'),
        ),
        migrations.AlterField(
            model_name='company',
            name='zoon_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Zoon'),
        ),
    ]
