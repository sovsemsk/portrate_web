# Generated by Django 4.2.5 on 2023-11-11 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0005_remove_notification_url_alter_notification_initiator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='dikidi_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='dikidi_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='dikidi_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='flamp_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='flamp_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='flamp_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='gis_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='gis_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='gis_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='google_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='google_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='google_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='irecommend_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='irecommend_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='irecommend_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='mapsme_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='mapsme_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='mapsme_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='otzovik_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='otzovik_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='otzovik_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='portrate_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='portrate_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='prodoctorov_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='prodoctorov_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='prodoctorov_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='restoclub_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='restoclub_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='restoclub_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='total_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='total_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='tripadvisor_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='tripadvisor_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='tripadvisor_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='yandex_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='yandex_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='yandex_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='zoon_negative_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='zoon_positive_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='zoon_rate',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=1, null=True),
        ),
    ]