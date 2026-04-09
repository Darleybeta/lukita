from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, VentaViewSet, VentaDetalleViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'ventas', VentaViewSet, basename='venta')
router.register(r'ventas-detalle', VentaDetalleViewSet, basename='venta-detalle')

urlpatterns = [
    path('', include(router.urls)),
]