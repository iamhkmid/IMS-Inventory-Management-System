from django import template
register = template.Library()

@register.simple_tag()
def total_rupiah(jumlah_awal, masuk, keluar, nilai_barang, *args, **kwargs):
    # you would need to do any localization of the result here
    result = '{:,.0f}'.format((jumlah_awal + masuk - keluar)* nilai_barang).replace(',', '.')
    return result

@register.simple_tag()
def total_jumlah(jumlah_awal, masuk, keluar, *args, **kwargs):
    # you would need to do any localization of the result here
    result = '{:,.0f}'.format(jumlah_awal + masuk - keluar)
    return result

@register.simple_tag()
def total_rupiah_min(jumlah_awal, nilai_barang, *args, **kwargs):
    # you would need to do any localization of the result here
    result = '{:,.0f}'.format(jumlah_awal * nilai_barang).replace(',', '.')
    return result