from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(value, delimiter):
    if value is None:
        return []
    return value.split(delimiter)

@register.filter
def last_item(value):
    try:
        return value[-1]
    except (IndexError, TypeError, AttributeError): # AttributeError for None
        return None
        
@register.filter # 新增 first_item 過濾器，用於 watch?v= 的情況
def first_item(value):
    try:
        return value[0]
    except (IndexError, TypeError, AttributeError):
        return None