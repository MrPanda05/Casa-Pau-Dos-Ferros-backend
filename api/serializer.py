import django.contrib.auth.models
from rest_framework import serializers
from .models import user as le_user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = le_user
        fields = ['username', 'email', 'password', 'date', 'cpf']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = le_user.objects.create_user(**validated_data)
        return user