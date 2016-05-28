from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value):
    """Removes all values of arg from the given string"""
    v = str(value)
    return v.replace(',', '.')