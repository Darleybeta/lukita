from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NominaViewSet, NominaConceptoViewSet

router = DefaultRouter()
router.register(r'', NominaViewSet, basename='nomina')
router.register(r'conceptos', NominaConceptoViewSet, basename='concepto')

urlpatterns = [
    path('', include(router.urls)),
]