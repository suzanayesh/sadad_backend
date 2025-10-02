from rest_framework import serializers
from .models import RootUser

class RootUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RootUser
        fields = ['id', 'username', 'password_hash']
