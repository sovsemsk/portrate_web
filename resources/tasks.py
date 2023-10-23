import asyncio
from celery import shared_task
from django.conf import settings
from telegram import Bot
from resources.models import NegativeMessage


@shared_task
def notify_subcrition_created(telegram_id):
    bot = Bot(settings.TELEGRAM_BOT_API_SECRET)
    asyncio.run(bot.send_message(
        telegram_id, 'Вы подписаны на уведомления'
    ))


@shared_task
def notify_negative_message(negative_message_id):
    negative_message = NegativeMessage.objects.filter(
        id=negative_message_id
    ).first()

    if not negative_message:
        return

    tags = ''
    for tag in negative_message.negative_message_tag.all():
        tags += f'{tag.text}, '

    for user in negative_message.company.user.exclude(profile__telegram_id=None).all():
        bot = Bot(settings.TELEGRAM_BOT_API_SECRET)
        asyncio.run(bot.send_message(
            user.profile.telegram_id, f'''Негативное сообщение в Портрете.

Теги:
{tags[:len(tags) - 2]}

Телефон:
{negative_message.phone}

Комментарий:
{negative_message.text}'''
        ))
