from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.root_users.models import RootUser


def _get_token_serializer():
    try:
        from rest_framework_simplejwt.serializers import \
            TokenObtainPairSerializer as _serializer
        return _serializer
    except Exception:
        return None


class RootTokenObtainPairView(APIView):
    """POST /api/token/ - issues access and refresh tokens for RootUser"""

    def post(self, request, *args, **kwargs):
        data = request.data or {}
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return Response({'detail': 'username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            root = RootUser.objects.get(username=username)
        except RootUser.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, root.password_hash):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = _get_token_serializer()
        if not serializer:
            return Response({'detail': 'simplejwt not installed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token = serializer.get_token(root)
        token['root_id'] = root.id
        access = str(token.access_token)
        refresh = str(token)

        return Response({'access': access, 'refresh': refresh}, status=status.HTTP_200_OK)
