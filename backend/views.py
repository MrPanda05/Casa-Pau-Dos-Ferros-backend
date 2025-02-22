from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.files.base import ContentFile
import base64

from api.models import *
from api.serializer import *
from .pagination import *

class AddressViewSet(viewsets.ModelViewSet):
    queryset = user_address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = get_list_or_404(user_address, user_id=request.user.id)
        # serializer = AddressSerializer(queryset, many=True)
        pagination_class = StandardPagination()
        page = pagination_class.paginate_queryset(queryset, request)
        if page is not None:
            serializer = AddressSerializer(page, many=True)
            return pagination_class.get_paginated_response(serializer.data)
        return Response('No addresses registered', status=404)
    
    def retrieve(self, request, pk=None):
        address = get_object_or_404(user_address, user_id=request.user.id, address_id=pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)
    
    
    def create(self, request):
        serializer = AddressSerializer(data=request.data)
        serializer.context['request'] = request
        if(serializer.is_valid()):
            serializer.save()
            return Response({"message": "Address registered!"}, status=201)
        return Response(serializer.errors, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination


class StaffViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = StaffUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardPagination

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated&IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = Product.objects.all()
        pagination_class = ProductPagination()
        page = pagination_class.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return pagination_class.get_paginated_response(serializer.data)
        return Response('No products registered', status=404)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, product_id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def create(self, request):
        if(request.data['image'] not in (None, '')):
            format, imgstr = request.data['image'].split(';base64,') 
            ext = format.split('/')[-1]
            request.data['image'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        serializer = ProductSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"message": "Product registered!"}, status=201)
        return Response(serializer.errors, status=400)
    
    def update(self, request, *args, **kwargs):
        if(request.data['image'] not in (None, '')):
            format, imgstr = request.data['image'].split(';base64,')
            fileName = str(request.data['product_id'])
            ext = format.split('/')[-1]
            request.data['image'] = ContentFile(base64.b64decode(imgstr), name=fileName + '.' + ext)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardPagination

    def list(self, request):
        queryset = Category.objects.all()
        pagination_class = StandardPagination()
        page = pagination_class.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CategorySerializer(page, many=True)
            return pagination_class.get_paginated_response(serializer.data)
        return Response('No categories registered', status=404)

    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, category_id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"message": "Category registered!"}, status=201)
        
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    pagination_class = StandardPagination

    def list(self, request):
        queryset = ProductCategory.objects.all()
        pagination_class = StandardPagination()
        page = pagination_class.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProductCategorySerializer(page, many=True)
            return pagination_class.get_paginated_response(serializer.data)
        return Response('No product categories registered', status=404)