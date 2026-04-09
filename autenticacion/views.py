from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario

def get_tokens_for_user(usuario):
    refresh = RefreshToken()
    refresh['id'] = usuario.id
    refresh['correo'] = usuario.correo
    refresh['rol'] = usuario.rol
    refresh['negocio_id'] = usuario.negocio_id
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    correo = request.data.get('correo')
    password = request.data.get('password')

    if not correo or not password:
        return Response(
            {'error': 'Correo y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        usuario = Usuario.objects.get(correo=correo)
    except Usuario.DoesNotExist:
        return Response(
            {'error': 'Usuario no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not check_password(password, usuario.contrasena):
        return Response(
            {'error': 'Contraseña incorrecta'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    tokens = get_tokens_for_user(usuario)
    return Response({
        'mensaje': 'Login exitoso',
        'tokens': tokens,
        'usuario': {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            'rol': usuario.rol,
            'negocio_id': usuario.negocio_id
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def registro(request):
    nombre = request.data.get('nombre')
    correo = request.data.get('correo')
    password = request.data.get('password')
    rol = request.data.get('rol', 'empleado')

    if not nombre or not correo or not password:
        return Response(
            {'error': 'Nombre, correo y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if Usuario.objects.filter(correo=correo).exists():
        return Response(
            {'error': 'Ya existe un usuario con ese correo'},
            status=status.HTTP_400_BAD_REQUEST
        )

    usuario = Usuario.objects.create(
        nombre=nombre,
        correo=correo,
        contrasena=make_password(password),
        rol=rol
    )

    tokens = get_tokens_for_user(usuario)
    return Response({
        'mensaje': 'Usuario creado exitosamente',
        'tokens': tokens,
        'usuario': {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            'rol': usuario.rol
        }
    }, status=status.HTTP_201_CREATED)