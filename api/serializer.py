import base64
from django.core.files import File
from rest_framework import serializers
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'birth_date', 'cpf', 'id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'cpf', 'is_staff', 'id']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['is_staff'] = True
        user = User.objects.create_user(**validated_data)
        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_address
        fields = ['address_id', 'user_id', 'cep', 'state', 'city', 'street', 'number', 'complement']
        extra_kwargs = {
            'address_id': {'read_only': True},
            'user_id': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        address = user_address.objects.create(**validated_data)
        return address
    
class ProductSerializer(serializers.ModelSerializer):
    base64_image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'price', 'amount', 'image', 'base64_image']
        extra_kwargs = {
            'product_id': {'read_only': True},
        }
    def get_base64_image(self, obj):
        if obj.image:
            with open(obj.image.path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        return None

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name', 'description']
        extra_kwargs = {
            'category_id': {'read_only': True},
        }
    
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category
    
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'category', 'product']
        extra_kwargs = {
            'id': {'read_only': True},
        }
    
    def create(self, validated_data):
        product_category = ProductCategory.objects.create(**validated_data)
        return product_category

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['cart_id', 'user_id', 'is_active']
        extra_kwargs = {
            'cart_id': {'read_only': True},
            'user_id': {'read_only': True},
            'is_active': {'read_only': True}
        }
    
    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        cart = Cart.objects.create(**validated_data)
        return cart

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']
        extra_kwargs = {
            'id': {'read_only': True},
            'cart': {'read_only': True},
            'quantity': {'required': True}
        }

    def create(self, validated_data):
        validated_data['cart'] = self.context['cart']
        cart_item = CartItem.objects.create(**validated_data)
        return cart_item