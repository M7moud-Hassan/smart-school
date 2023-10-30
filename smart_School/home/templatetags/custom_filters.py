from django import template

register = template.Library()

@register.filter
def get_item(value, index):
    try:
        return value[index]
    except (IndexError, TypeError):
        return None
