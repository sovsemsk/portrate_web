# Generated by Django 4.2.5 on 2023-10-16 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_alter_negativemessage_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NegativeMessageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=255, verbose_name='текст тега')),
            ],
            options={
                'verbose_name': 'тег негативного сообщения',
                'verbose_name_plural': 'теги негативного сообщения',
                'db_table': 'feedback_negative_message_tag',
            },
        ),
        migrations.AlterModelOptions(
            name='negativereview',
            options={'verbose_name': 'негативный отзыв', 'verbose_name_plural': 'негативные отзывы'},
        ),
        migrations.AlterModelOptions(
            name='positivereview',
            options={'verbose_name': 'позитивный отзыв', 'verbose_name_plural': 'позитивные отзывы'},
        ),
        migrations.AlterField(
            model_name='negativemessage',
            name='phone',
            field=models.CharField(max_length=255, verbose_name='контактный телефон'),
        ),
        migrations.AlterField(
            model_name='negativemessage',
            name='text',
            field=models.TextField(blank=True, verbose_name='текст сообщения'),
        ),
        migrations.AddField(
            model_name='negativemessage',
            name='negative_message_tag',
            field=models.ManyToManyField(blank=True, to='feedback.negativemessagetag', verbose_name='теги негативных сообщений'),
        ),
    ]