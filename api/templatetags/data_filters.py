#HTML sayfaları için fonksiyonlar
from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    if isinstance(arg, str):
        if ',' in arg:
            old, new = arg.split(",", 1)
        elif '|' in arg:
            old, new = arg.split("|", 1)
        else:
            return value.replace(arg, " ")
        return value.replace(old, new)
    return value



@register.filter(name='get_item')
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(key)
    else:
        return None