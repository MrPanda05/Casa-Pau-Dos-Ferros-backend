from rest_framework import serializers
from .models import User, user_address
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'birth_date', 'cpf']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_address
        fields = ['address_id', 'user_id', 'cep', 'state', 'city', 'street', 'number', 'complement']
        extra_kwargs = {
            'address_id': {'read_only': True}
        }

    def create(self, validated_data):
        address = user_address.objects.create(**validated_data)
        return address