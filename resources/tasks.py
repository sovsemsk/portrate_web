import asyncio
from celery import shared_task
from django.conf import settings
from resources.models import NegativeMessage


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
        print(user.profile.telegram_id)
        asyncio.run(settings.TELEGRAM_BOT.send_message(
            user.profile.telegram_id, f'У вас новое негативное сообщение в Портрете\r\nТеги:\r\n{tags}\r\nТелефон: {negative_message.phone}\r\nКомментарий: \r\n{negative_message.text}'
        ))
