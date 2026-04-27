from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            usuario = Usuario.objects.get(id=user_id)
            return usuario
        except Usuario.DoesNotExist:
            raise InvalidToken('User not found')
def get_tokens_for_user(usuario):
    refresh = RefreshToken()
    refresh['user_id'] = usuario.id  # ← cambia 'id' por 'user_id'
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

    negocio_id = request.data.get('negocio_id')

    usuario = Usuario.objects.create(
        nombre=nombre,
        correo=correo,
        contrasena=make_password(password),
        rol=rol,
        negocio_id=negocio_id
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
@api_view(['GET'])
def listar_usuarios(request):
    negocio_id = request.query_params.get('negocio_id')
    if negocio_id:
        usuarios = Usuario.objects.filter(negocio_id=negocio_id).values(
            'id', 'nombre', 'correo', 'telefono', 'rol'
        )
    else:
        usuarios = Usuario.objects.all().values(
            'id', 'nombre', 'correo', 'telefono', 'rol'
        )
    return Response(list(usuarios))
@api_view(['DELETE', 'PATCH'])
def gestionar_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        usuario.delete()
        return Response({'mensaje': 'Usuario eliminado'}, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        if 'nombre' in request.data:
            usuario.nombre = request.data['nombre']
        if 'correo' in request.data:
            usuario.correo = request.data['correo']
        if 'rol' in request.data:
            usuario.rol = request.data['rol']
        usuario.save()
        return Response({'id': usuario.id, 'nombre': usuario.nombre, 'correo': usuario.correo, 'rol': usuario.rol})