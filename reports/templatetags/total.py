from django import template
register = template.Library()

@register.inclusion_tag('reports/report_persediaan.html', takes_context=True)
def session(context):
    #request = context['request']
    request = context['request']
    a = request.session['satker']
    print(a)
    return a