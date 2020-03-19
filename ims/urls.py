from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('transaksi/', include('transaksi.urls', namespace='transaksi')),
    path('satker/', include('satker.urls', namespace='satker')),
    path('report/', include('reports.urls', namespace='report')),
    path('', RedirectView.as_view(pattern_name='inventory:barang_list')),
    path('test/',TemplateView.as_view(template_name='test.html')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
