from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404

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

    def get_base64_image(self, obj):
        f = open(obj.image.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data

    def list(self, request):
        queryset = Product.objects.all()
        pagination_class = ProductPagination()
        page = pagination_class.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            for product in serializer.data:
                product['base64_image'] = self.get_base64_image(Product.objects.get(product_id=product['product_id']))
            return pagination_class.get_paginated_response(serializer.data)
        return 
