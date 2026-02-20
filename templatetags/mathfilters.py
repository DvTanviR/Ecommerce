from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def mex(value):
    return value * 20