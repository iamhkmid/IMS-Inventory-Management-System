from django import template

register = template.Library()

@register.filter
def modulus(num, val):
    return num % val == 0.5