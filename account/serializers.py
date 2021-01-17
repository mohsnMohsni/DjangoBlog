from rest_framework import serializers
from .models import User
from .validators import password_validator
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user and get password for register and show other field
    """
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'is_staff', 'is_active', 'password', 'confirm_password')
        extra_kwargs = {
            'id': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate(self, data):
        password1 = data['password']
        password2 = data['confirm_password']
        password_validator(password1, password2)
        return data

    def create(self, validated_data):
        password = validated_data['password']
        validated_data.pop('confirm_password', None)
        validated_data['is_active'] = True
        validated_data['password'] = make_password(password)
        return super(UserSerializer, self).create(validated_data)
