from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.files.base import ContentFile
import base64
from decimal import Decimal

from api.models import *
from api.serializer import *
from .pagination import *

# Adicionando produto
    # checar se quantiade está disponível
# Alterando quantiade
    # remover quantiade que estava atenriormente
    # checar se quantidade está disponível

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
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk=None):
        cart = get_object_or_404(Cart, user_id=request.user.id, is_active=True)
        cart.is_active = False
        cart.status = Cart.Status.Canceled
        cart.save()
        return Response({"message": "Cart deactivated!"}, status=200)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart = get_object_or_404(Cart, user_id=request.user.id, is_active=True, status=Cart.Status.Open)
        queryset = CartItem.objects.filter(cart_id=cart.cart_id)
        pagination_class = StandardPagination()
        page = pagination_class.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CartItemSerializer(page, many=True)
            return pagination_class.get_paginated_response(serializer.data)
        return Response('No products in the cart', status=404)

    def create(self, request):
        #check for active cart
        cart = Cart.objects.get_or_create(user_id=request.user, is_active=True, status=Cart.Status.Open)[0]
        product = get_object_or_404(Product, product_id=request.data['product'])
        if request.data['quantity'] not in (None, ''):
            #check if product is already in the cart
            cart_item = CartItem.objects.filter(cart_id=cart.cart_id, product_id=product.product_id)
            if cart_item:
                return Response({"message": "Product already in the cart!"}, status=400)
            #check if product amount is available
            req_amount = Decimal(request.data['quantity'])
            if (product.amount-product.reserved) < req_amount:
                return Response({"message": "Product amount not available | stock: " + str(product.amount-product.reserved)}, status=400)
            else:
                product.reserved += req_amount
        serializer = CartItemSerializer(data=request.data, context={'cart': cart})
        if(serializer.is_valid()):
            serializer.save()
            product.save()
            return Response({"message": "Product added to the cart !"}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        cart = get_object_or_404(Cart, user_id=request.user.id, is_active=True)
        cart_item = get_object_or_404(CartItem, id=pk)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        cart = get_object_or_404(Cart, user_id=request.user.id, is_active=True)
        cart_item = get_object_or_404(CartItem, id=pk)
        product = get_object_or_404(Product, product_id=cart_item.product.product_id)
        if request.data['product'] not in (None, '') and request.data['product'] != cart_item.product.product_id:
            aux_product = get_object_or_404(Product, product_id=request.data['product'])
            #validate if product is already in the cart
            if(aux_product != product):
                cart_item_aux = CartItem.objects.filter(cart_id=cart.cart_id, product_id=aux_product.product_id)
                if cart_item_aux:
                    return Response({"message": "Product already in the cart!"}, status=400)
            #validate product change
            if((aux_product.amount-aux_product.reserved) < cart_item.quantity):
                return Response({"message": "Product amount not available | stock: " + str(aux_product.amount-aux_product.reserved)}, status=400)
            else:
                product.reserved -= cart_item.quantity
                aux_product.reserved += cart_item.quantity
                product, aux_product = aux_product, product
        #validate quantity change
        if request.data['quantity'] not in (None, ''):
            if Decimal(request.data['quantity']) != cart_item.quantity:
                # remove older quantity
                product.reserved -= cart_item.quantity
                # validate newer quantity
                req_amount = Decimal(request.data['quantity'])
                if (product.amount-product.reserved) < req_amount:
                    return Response({"message": "Product amount not available | stock: " + str(product.amount-product.reserved)}, status=400)
                else:
                    product.reserved += req_amount
        serializer = CartItemSerializer(cart_item, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            product.save()
            if(aux_product != None):
                aux_product.save()
            return Response({"message": "Product updated in the cart " + str(cart.cart_id) + " !"}, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        cart = get_object_or_404(Cart, user_id=request.user.id, is_active=True)
        cart_item = get_object_or_404(CartItem, id=pk)
        # remove product reserve
        product = get_object_or_404(Product, product_id=cart_item.product.product_id)
        product.reserved -= cart_item.quantity
        product.save()
        cart_item.delete()
        cart_items = CartItem.objects.filter(cart_id=cart.cart_id)
        if not cart_items:
            cart.is_active = False
            cart.status = Cart.Status.Canceled
            cart.save()
            return Response({"message": "Product removed from the cart " + str(cart.cart_id) + " and cart deactivated!"}, status=200)
        return Response({"message": "Product removed from the cart " + str(cart.cart_id) + " !"}, status=200)