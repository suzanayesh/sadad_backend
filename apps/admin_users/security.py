from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.root_users.models import RootUser


def _lazy_import_simplejwt():
    # delay import until runtime to avoid hard dependency at import-time
    from rest_framework_simplejwt.authentication import \
        JWTAuthentication as _jwt_auth
    from rest_framework_simplejwt.serializers import \
        TokenObtainPairSerializer as _token_serializer
    from rest_framework_simplejwt.views import \
        TokenRefreshView as _refresh_view

    return _token_serializer, _refresh_view, _jwt_auth


class RootTokenObtainPairView(APIView):
    """POST /api/token/ - returns { access, refresh } for a RootUser

    Body: { "username": "...", "password": "..." }
    """

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

        _token_serializer, _refresh_view, _jwt_auth = _lazy_import_simplejwt()
        token = _token_serializer.get_token(root)
        token['root_id'] = root.id

        access = str(token.access_token)
        refresh = str(token)

        return Response({'access': access, 'refresh': refresh}, status=status.HTTP_200_OK)


class RootJWTAuthentication:
    """Authentication class that uses simplejwt to validate tokens and resolves
    the `root_id` claim to a `RootUser` instance (set as request.user).
    """

    def __init__(self):
        _, _, _jwt_auth = _lazy_import_simplejwt()
        self._base = _jwt_auth()

    def authenticate(self, request):
        result = self._base.authenticate(request)
        if not result:
            return None
        # result is (django_user, validated_token) per simplejwt
        _, validated_token = result
        root_id = validated_token.get('root_id')
        if not root_id:
            return None
        try:
            root = RootUser.objects.get(id=root_id)
        except RootUser.DoesNotExist:
            return None

        return (root, validated_token)

