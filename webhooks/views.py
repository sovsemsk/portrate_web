import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from resources.models import Branch
from webhooks.models import TelegramSubscription


@csrf_exempt
@require_http_methods(['POST'])
def webhooks_telegram_update(request):
    # @TODO: Добавить авторизацию
    update = json.loads(request.body)

    # Безопасно заберем данные
    telegram_user_id = update.get('message', {}).get('from', {}).get('id')
    api_secret = update.get('message', {}).get('text').replace('/start ', '')

    #
    branch = Branch.objects.filter(api_secret=api_secret).first()

    if (branch):
        TelegramSubscription.objects.create(
            telegram_user_id=telegram_user_id,
            group=branch.group,
            branch=branch
        )

    return (HttpResponse('ok'))
