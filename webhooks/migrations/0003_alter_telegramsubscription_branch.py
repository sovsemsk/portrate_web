# Generated by Django 4.2.5 on 2023-10-20 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0027_alter_branch_api_secret'),
        ('webhooks', '0002_telegramsubscription_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramsubscription',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.branch', verbose_name='филиал'),
        ),
    ]