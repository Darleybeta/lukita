from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentoViewSet, ProveedorViewSet, CategoriaViewSet, ClienteViewSet

router = DefaultRouter()
router.register(r'documentos', DocumentoViewSet, basename='documento')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'clientes', ClienteViewSet, basename='cliente')

urlpatterns = [
    path('', include(router.urls)),
]