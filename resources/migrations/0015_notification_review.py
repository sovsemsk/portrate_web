# Generated by Django 4.2.5 on 2023-11-20 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0014_alter_review_remote_id_alter_review_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='review',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resources.review', verbose_name='отзыв'),
        ),
    ]