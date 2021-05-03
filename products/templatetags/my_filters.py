from django import template

register = template.Library()

@register.filter(name='count')
def count(length):
    """returning list with the given length"""
    return list(range(length))