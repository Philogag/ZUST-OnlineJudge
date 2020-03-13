from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'user_level'
        ]

class UserAuthOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = [
            'username',
            'token',
        ]

