# Generated by Django 5.0.4 on 2024-10-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0026_rename_count_avito_company_reviews_count_remote_avito_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='feedback_text_create_heading',
            field=models.CharField(default='Написать директору', verbose_name='заголовок страницы создания жалобы'),
        ),
        migrations.AddField(
            model_name='company',
            name='feedback_text_rate_heading',
            field=models.CharField(default='Вам понравилось обслуживание?', verbose_name='заголовок главной страницы'),
        ),
        migrations.AddField(
            model_name='company',
            name='feedback_text_request_heading',
            field=models.CharField(default='Наградите нас отзывом?', verbose_name='заголовок страницы запрос отзывов'),
        ),
        migrations.AddField(
            model_name='company',
            name='feedback_text_success_heading',
            field=models.CharField(default='Ваше сообщение отправлено', verbose_name='заголовок страницы после оставления жалобы'),
        ),
        migrations.AddField(
            model_name='company',
            name='feedback_text_success_text',
            field=models.CharField(default='Спасибо за обращение, в близжайшее время с вами свяжется наш администратор по указанному вам телефону.', verbose_name='текст страницы после оставления жалобы'),
        ),
    ]