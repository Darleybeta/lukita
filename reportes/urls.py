from django.urls import path
from . import views

urlpatterns = [
    path('resumen/', views.resumen_financiero),
    path('bajo-stock/', views.productos_bajo_stock),
    path('por-categoria/', views.transacciones_por_categoria),
]