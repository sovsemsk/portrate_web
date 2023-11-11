from django import template

register = template.Library() 

@register.filter
def sum(a,b):
    return int(a) + int(b)