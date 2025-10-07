from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import RootUser


class RootUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RootUser
        fields = ["id", "username", "password_hash"]

    def create(self, validated_data):
        validated_data["password_hash"] = make_password(validated_data["password_hash"])
        return super().create(validated_data)


class UpdateRootPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RootUser
        fields = ["username", "password_hash"]

    def update(self, instance, validated_data):
        instance.password_hash = make_password(validated_data.get("password_hash"))
        instance.save()
        return instance
