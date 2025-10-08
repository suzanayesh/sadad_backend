from rest_framework import serializers

from apps.admin_users.models import AdminUser
from apps.root_users.models import RootUser


class RootSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = RootUser
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = RootUser(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'password', 'root']

    def create(self, validated_data):
        user = AdminUser(username=validated_data['username'], root=validated_data['root'])
        user.set_password(validated_data['password'])
        user.save()
        return user
