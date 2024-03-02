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