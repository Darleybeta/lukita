from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('registro/', views.registro),
    path('usuarios/', views.listar_usuarios),
    path('usuarios/<int:usuario_id>/', views.gestionar_usuario),
]