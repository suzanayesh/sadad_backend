from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from .models import RootUser
from .serializers import RootUserSerializer
from apps.admin_users.serializers import RootLoginSerializer


class RootLoginView(APIView):
    """POST /api/root/login/ - returns a token for the root user

    Body: { "username": "...", "password": "..." }
    Response: { "token": "..." }
    """

    def post(self, request, *args, **kwargs):
        serializer = RootLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.create_token()
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class CreateRootUserView(generics.CreateAPIView):
    queryset = RootUser.objects.all()
    serializer_class = RootUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            "Root user added successfully ✅",
            status=status.HTTP_201_CREATED
        )
class UpdateRootPasswordView(APIView):
    """Update a RootUser's password by root_id.

    URL: PUT /api/root/<root_id>/updaterootpassword/
    Body (JSON): { "password_hash": "new-plain-password" }
    """

    def put(self, request, root_id=None, *args, **kwargs):
        new_password = request.data.get("password_hash")

        if not new_password:
            return Response("password_hash is required ❌", status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(RootUser, id=root_id)
        user.password_hash = make_password(new_password)
        user.save()

        return Response("Password updated successfully ✅", status=status.HTTP_200_OK)


class DeleteRootUserView(APIView):
    """Delete a RootUser by username.

    Accepts either:
    - DELETE /api/deleterootuser/?username=alice
    - DELETE /api/deleterootuser/ with JSON body { "username": "alice" }
    """

    def delete(self, request, *args, **kwargs):
        username = request.query_params.get("username") or request.data.get("username")

        if not username:
            return Response("username is required ❌", status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(RootUser, username=username)
        user.delete()

        return Response("Root user deleted successfully ✅", status=status.HTTP_200_OK)
