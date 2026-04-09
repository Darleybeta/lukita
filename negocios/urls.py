from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NegocioViewSet, SolicitudViewSet

router = DefaultRouter()
router.register(r'', NegocioViewSet)
router.register(r'solicitudes', SolicitudViewSet)

urlpatterns = [
    path('', include(router.urls)),
]