from django import template
register = template.Library()

@register.simple_tag()
def jumlah(masuk, keluar, *args, **kwargs):
    # you would need to do any localization of the result here
    result = '{:,.0f}'.format(masuk - keluar)
    return result