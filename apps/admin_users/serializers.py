import secrets

from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers

from apps.root_users.models import RootUser

from .models import AdminRequest, AdminUser, RootUserToken


class AdminRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRequest
        fields = [
            "id",
            "first_name",
            "last_name",
            "national_id",
            "phone",
            "email",
            "status",
            "requested_at",
        ]
        # Admin creates requests without root_user; status and requested_at are read-only
        read_only_fields = ["id", "status", "requested_at"]


class CreateAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ["id", "username", "password_hash", "first_name", "last_name", "national_id", "phone", "email", "root_user"]
        read_only_fields = ["id", "root_user"]

    def create(self, validated_data):
        # hash the provided password
        validated_data["password_hash"] = make_password(validated_data["password_hash"])
        return super().create(validated_data)


class RootPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)


class RootLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        try:
            root = RootUser.objects.get(username=username)
        except RootUser.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not check_password(password, root.password_hash):
            raise serializers.ValidationError("Invalid credentials")

        attrs["root"] = root
        return attrs

    def create_token(self):
        root = self.validated_data["root"]
        # generate a secure random token
        key = secrets.token_hex(32)
        token = RootUserToken.objects.create(key=key, root_user=root)
        return token

