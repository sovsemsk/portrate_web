# Generated by Django 5.0.2 on 2024-03-12 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0030_alter_company_parser_link_gis_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'verbose_name': 'сообщение', 'verbose_name_plural': 'сообщения'},
        ),
        migrations.AddField(
            model_name='company',
            name='messages_total_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество сообщений'),
        ),
        migrations.AddField(
            model_name='company',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='Общий рейтинг'),
        ),
        migrations.AddField(
            model_name='company',
            name='rating_gis',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг 2Гис'),
        ),
        migrations.AddField(
            model_name='company',
            name='rating_gis_last_parse_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата последней загрузки рейтинга 2Гис'),
        ),
        migrations.AddField(
            model_name='company',
            name='rating_google',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Google'),
        ),
        migrations.AddField(
            model_name='company',
            name='rating_google_last_parse_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата последней загрузки рейтинга Google'),
        ),
        migrations.AddField(
            model_name='company',
            name='rating_yandex',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=10, null=True, verbose_name='рейтинг Яндекс'),
        ),
        migrations.AddField(
            model_name='company',
            name='rating_yandex_last_parse_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата последней загрузки рейтинга Яндекс'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_gis_last_parse_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата последней загрузки отзывов 2Гис'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_gis_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество негативных отзывов 2Гис'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_gis_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество позитивных отзывов 2Гис'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_gis_total_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество отзывов 2Гис'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_google_last_parse_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата последней загрузки отзывов Google'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_google_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество негативных отзывов Google'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_google_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество позитивных отзывов Google'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_google_total_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество отзывов Google'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество негативных отзывов'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество позитивных отзывов'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_total_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество отзывов'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_yandex_last_parse_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата последней загрузки отзывов Яндекс'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_yandex_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество негативных отзывов Яндекс'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_yandex_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество позитивных отзывов Яндекс'),
        ),
        migrations.AddField(
            model_name='company',
            name='reviews_yandex_total_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='количество отзывов Яндекс'),
        ),
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.IntegerField(blank=True, null=True, verbose_name='количество звезд'),
        ),
    ]