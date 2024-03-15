from django import template

register = template.Library() 

@register.filter
def sum(a,b):
    """
    Суммирует 2 числа

    {{someval|sum:someval}}
    """
    return a + b


@register.filter(is_safe=False)
def rupluralize(value, forms):
    """
    Подбирает окончание существительному после числа

    {{someval|rupluralize:"отзыв, отзыва, отзывов"}}
    """
    try:
        one, two, many = forms.split(u",")
        value = str(value)[-2:]  # 314 -> 14

        if (21 > int(value) > 4):
            return many

        if value.endswith("1"):
            return one
        elif value.endswith(("2", "3", "4")):
            return two
        else:
            return many

    except (ValueError, TypeError):
        return ""

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Возвращает закодированные параметры URL, которые совпадают с текущими
    параметры запроса, только с добавлением или изменением указанных параметров GET.
    Он также удаляет любые пустые параметры, чтобы все было аккуратно.
    поэтому вы можете удалить параметр, установив для него значение ``""``.

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    Основано на
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()