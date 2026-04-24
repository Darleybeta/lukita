from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import Usuario

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            usuario = Usuario.objects.get(id=user_id)
            return usuario
        except Usuario.DoesNotExist:
            raise InvalidToken('User not found')