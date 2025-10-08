from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.admin_users.models import AdminUser
from apps.root_users.models import RootUser

from .jwt import get_tokens_for_user


class LoginView(APIView):
    """
    Authenticates either a RootUser or AdminUser and returns JWT tokens.
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        role = None

        # Try RootUser first
        try:
            user = RootUser.objects.get(username=username)
            role = "root"
        except RootUser.DoesNotExist:
            # Try AdminUser if not a root
            try:
                user = AdminUser.objects.get(username=username)
                role = "admin"
            except AdminUser.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Password check (both Root and Admin have check_password)
        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens
        tokens = get_tokens_for_user(user)
        tokens["role"] = role
        return Response(tokens, status=status.HTTP_200_OK)


class CreateAdminView(APIView):
    """
    Allows only authenticated RootUsers (via JWT) to create new Admin accounts.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, "role") or request.user.role != "root":
            return Response({"error": "Permission denied. Only root users can create admins."}, status=status.HTTP_403_FORBIDDEN)

        from apps.admin_users.serializers import CreateAdminUserSerializer

        serializer = CreateAdminUserSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save(root_user=request.user)
            data = {
                "id": admin.id,
                "username": admin.username,
                "email": admin.email,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
