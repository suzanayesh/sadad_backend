from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.root_users.models import RootUser

from .models import AdminRequest, AdminUser
from .serializers import (AdminRequestSerializer, CreateAdminUserSerializer,
                          RootPasswordSerializer)


class CreateAdminRequestGlobalView(APIView):
		"""POST /api/create-admin-request/ - accepts root_id in body and applicant fields

		Body JSON example:
		{
			"root_id": 1,
			"first_name": "Ahmad",
			"last_name": "Saleh",
			"national_id": "987654321",
			"phone": "0599123456",
			"email": "ahmad@example.com"
		}
		"""

		def post(self, request, *args, **kwargs):
				# Admins submit requests without root assignment
				serializer = AdminRequestSerializer(data=request.data)
				serializer.is_valid(raise_exception=True)
				serializer.save()
				return Response("Admin request submitted successfully ✅", status=status.HTTP_201_CREATED)


class CreateAdminRequestView(generics.CreateAPIView):
	"""(deprecated) per-root admin request creation. Keep for compatibility but creates unassigned request."""
	serializer_class = AdminRequestSerializer

	def create(self, request, root_id=None, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response("Admin request submitted successfully ✅", status=status.HTTP_201_CREATED)


class ListAdminRequestsView(generics.ListAPIView):
	"""GET /api/root/<root_id>/admin-requests/"""
	serializer_class = AdminRequestSerializer

	def get_queryset(self):
		# For a root user, return pending requests (global). Optionally filter by status query param.
		status_q = self.request.query_params.get("status")
		qs = AdminRequest.objects.all()
		if status_q:
			qs = qs.filter(status__iexact=status_q)
		else:
			qs = qs.filter(status__iexact="PENDING")

		return qs


class AllAdminRequestsView(generics.ListAPIView):
	"""GET /api/admin-requests/ - returns all admin requests. Optional query param: ?status=PENDING|APPROVED|REJECTED"""
	serializer_class = AdminRequestSerializer

	def get_queryset(self):
		qs = AdminRequest.objects.all()
		status_q = self.request.query_params.get("status")
		if status_q:
			qs = qs.filter(status__iexact=status_q)
		return qs


class CreateAdminAccountView(APIView):
	"""POST /api/root/<root_id>/createadminaccount/<request_id>/"""

	def post(self, request, root_id, request_id, *args, **kwargs):
		root = get_object_or_404(RootUser, id=root_id)  # ensure root exists
		admin_request = get_object_or_404(AdminRequest, id=request_id)

		if admin_request.status != "PENDING":
			return Response("Invalid request ❌", status=status.HTTP_400_BAD_REQUEST)

		username = request.data.get("username")
		password = request.data.get("password")
		if not username or not password:
			return Response("username and password are required ❌", status=status.HTTP_400_BAD_REQUEST)

		# create AdminUser using data from request
		admin_data = {
			"username": username,
			"password_hash": password,
			"first_name": admin_request.first_name,
			"last_name": admin_request.last_name,
			"national_id": admin_request.national_id,
			"phone": admin_request.phone,
			"email": admin_request.email,
			"root_user": root.id,
		}

		serializer = CreateAdminUserSerializer(data=admin_data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		admin_request.status = "APPROVED"
		admin_request.save()

		return Response("Admin account created successfully ✅", status=status.HTTP_201_CREATED)


class RejectAdminRequestView(APIView):
	"""PUT /api/root/<root_id>/reject-admin-request/<request_id>/"""

	def put(self, request, root_id, request_id, *args, **kwargs):
		get_object_or_404(RootUser, id=root_id)  # ensure root exists
		admin_request = get_object_or_404(AdminRequest, id=request_id)

		admin_request.status = "REJECTED"
		admin_request.save()

		return Response("Request rejected ❌", status=status.HTTP_200_OK)


class UpdateRootUserPasswordView(APIView):
	"""PUT /api/root/<root_id>/update-password/"""

	def put(self, request, root_id, *args, **kwargs):
		serializer = RootPasswordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		root = get_object_or_404(RootUser, id=root_id)
		root.password_hash = make_password(serializer.validated_data["password"])
		root.save()

		return Response("Password updated successfully ✅", status=status.HTTP_200_OK)


class DeleteRootUserView(APIView):
	"""DELETE /api/root/<root_id>/delete/"""

	def delete(self, request, root_id, *args, **kwargs):
		try:
			root = RootUser.objects.get(id=root_id)
		except RootUser.DoesNotExist:
			return Response("Root user not found ❌", status=status.HTTP_404_NOT_FOUND)

		root.delete()
		return Response("Root user deleted successfully ✅", status=status.HTTP_200_OK)

class CreateAdminByRootView(APIView):
    """
    POST /api/root/<int:root_id>/create-admin/

    Allows an authenticated root user to create a new admin account.
    Body:
    {
        "username": "admin123",
        "password": "strongpassword"
    }
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, root_id, *args, **kwargs):
        # Ensure authenticated root is the same as the one in the path
        if request.user.id != root_id:
            return Response(
                {"detail": "Unauthorized: you can only create admins under your own account ❌"},
                status=status.HTTP_403_FORBIDDEN
            )

        username = request.data.get("username")
        password = request.data.get("password")

        # Validate required fields
        if not username or not password:
            return Response(
                {"detail": "Both username and password are required ❌"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if username already exists
        if AdminUser.objects.filter(username=username).exists():
            return Response(
                {"detail": "This username already exists ❌"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new admin
        admin_data = {
            "username": username,
            "password_hash": make_password(password),
            "first_name": "",
            "last_name": "",
            "national_id": "",
            "phone": "",
            "email": "",
            "root_user": root_id,
        }

        admin = AdminUser.objects.create(**admin_data)

        response_data = {
            "id": admin.id,
            "username": admin.username,
            "root_user": admin.root_user.id,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)