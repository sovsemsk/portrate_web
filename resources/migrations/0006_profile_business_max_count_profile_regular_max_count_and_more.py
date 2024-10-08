# Generated by Django 5.0.4 on 2024-08-21 17:12

import djmoney.models.fields
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0005_alter_profile_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='business_max_count',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='максимальное количество филиалов тарифа Бизнес'),
        ),
        migrations.AddField(
            model_name='profile',
            name='regular_max_count',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='максимальное количество филиалов тарифа Стандарт'),
        ),
        migrations.AddField(
            model_name='profile',
            name='start_max_count',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='максимальное количество филиалов тарифа Старт'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='business_price_monthly_base',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('1500'), default_currency='RUB', max_digits=14, null=True, verbose_name='стоимость тарифа Бизнес, в месяц'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='regular_price_monthly_base',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('500'), default_currency='RUB', max_digits=14, null=True, verbose_name='стоимость тарифа Стандарт, в месяц'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='start_price_monthly_base',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default=Decimal('250'), default_currency='RUB', max_digits=14, null=True, verbose_name='стоимость тарифа Старт, в месяц'),
        ),
    ]
