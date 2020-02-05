from django import template
register = template.Library()

@register.simple_tag()
def total_nilai(jumlah_awal, masuk, keluar, nilai, *args, **kwargs):
    # you would need to do any localization of the result here
    result = '{:,.0f}'.format((jumlah_awal + masuk - keluar)* nilai).replace(',', '.')
    return result

@register.simple_tag()
def total_jumlah(jumlah_awal, masuk, keluar, *args, **kwargs):
    # you would need to do any localization of the result here
    result = '{:,.0f}'.format(jumlah_awal + masuk - keluar)
    return result