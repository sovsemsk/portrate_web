# Generated by Django 5.0.4 on 2024-08-28 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0011_payment_period'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'платеж', 'verbose_name_plural': 'платежи'},
        ),
    ]
