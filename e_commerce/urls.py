
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pedido/', include('pedido.urls')),
    # define o caminho(pedido?) das URL e inclue(include('pedido.urls')) elas de um arquivo especifico.
    path('perfil/', include('perfil.urls')),
    path('', include('produto.urls')),


]


if settings.DEBUG:  # interagem com as URL das imagens
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)