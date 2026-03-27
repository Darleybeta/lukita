from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('autenticacion.urls')),
    path('api/negocios/', include('negocios.urls')),
    path('api/contabilidad/', include('contabilidad.urls')),
    path('api/inventario/', include('inventario.urls')),
    path('api/nomina/', include('nomina.urls')),
    path('api/documentos/', include('documentos.urls')),
    path('api/reportes/', include('reportes.urls')),
    path('api/ia/', include('ia.urls')),
]