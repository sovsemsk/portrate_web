# Generated by Django 5.0.4 on 2024-09-16 19:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0016_alter_payment_api_secret'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='пользователи'),
        ),
        migrations.AlterField(
            model_name='review',
            name='remote_id',
            field=models.CharField(blank=True, db_index=True, null=True, verbose_name='ID (агрегация)'),
        ),
    ]