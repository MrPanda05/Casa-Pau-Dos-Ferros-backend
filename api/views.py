from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from .serializer import *
from .models import User
from backend.pagination import *

"""
Test
Args:
    HTTP request + AUTH
Returns:
    200 => {message}
"""
@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello from Django!"}, status=200)


"""
Register a new user 
Args:
    HTTP request
Returns:
    201 => {message}
    400 => {error}
"""
@api_view(["POST"])
def user_register(request):
    serializer = UserSerializer(data=request.data)

    if(serializer.is_valid()):
        serializer.save()
        return Response({"message": "Usuário registrado"}, status=201)
    return Response(serializer.errors, status=400)


"""
Logs user 
Args:
    HTTP request
Returns:
    200 => {token, username}
    400 => {message}
"""
@api_view(["POST"])
def user_login(request):
    login = request.data["login"]
    if "@" in login:
        userEmail = get_object_or_404(User, email=login)
        user = authenticate(username=userEmail.username, password=request.data["password"])
    else:
        user = authenticate(username=login, password=request.data["password"])
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "userId": user.id,
            "email": login,
            }, status=200)
    return Response({"message": "Credenciais inválidas"}, status=400)


"""
Logs user out of session
Args:
    HTTP request + AUTH
Returns:
    200 => {token}
"""
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Usuário desconectado"}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_add_address(request):
    serializer = AddressSerializer(data=request.data)
    serializer.context['request'] = request
    if(serializer.is_valid()):
        serializer.save()
        return Response({"message": "Endereço salvo com sucesso"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated&IsAdminUser])
def staff_register(request):
    serializer = StaffUserSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({"message": "Staff registrado com sucesso"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated&IsAdminUser])
def staff_Get(request):
    usermail = request.data["email"]
    UserAdmin = User.objects.filter(email=usermail).first()
    if(UserAdmin is None):
        return Response({"message": "Usuário não existe"}, status=400)
    isAdmin = UserAdmin.is_staff
    if(isAdmin):
        return Response({"message": "Usuário é staff"}, status=200)
    else:
        return Response({"message": "Usuário não é staff"}, status=200)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated&IsAdminUser])
def staff_Update(request):
    usermail = request.data["email"]
    UserAdmin = User.objects.filter(email=usermail).first()
    if(UserAdmin is None):
        return Response({"message": "Usuário não existe"}, status=400)
    isAdmin = UserAdmin.is_staff
    if(isAdmin):
        return Response({"message": "Usuário já é staff"}, status=200)
    else:
        UserAdmin.is_staff = True
        UserAdmin.save()
        return Response({"message": "Usuário registrado como staff"}, status=200)
    

    
@api_view(["POST"])
@permission_classes([IsAuthenticated&IsAdminUser])
def staff_Delete(request):
    usermail = request.data["email"]
    UserAdmin = User.objects.filter(email=usermail).first()
    if(UserAdmin is None):
        return Response({"message": "Usuário não encontrado"}, status=400)
    isAdmin = UserAdmin.is_staff
    if(not isAdmin):
        return Response({"message": "Usuário não é staff"}, status=200)
    else:
        UserAdmin.is_staff = False
        UserAdmin.save()
        return Response({"message": "Usuário não é mais staff"}, status=200)


@api_view(["GET"])
def productByCategory(request, category):
    queryset = ProductCategory.objects.filter(category=category)
    pagination_class = ProductPagination()
    page = pagination_class.paginate_queryset(queryset, request)
    if page is not None:
        aux = []
        for product in page:
            aux.append(product.product)
        serializer = ProductSerializer(aux, many=True)
        return pagination_class.get_paginated_response(serializer.data)
    return Response({"message": "Nenhum produto encontrado"}, status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirmCart(request):
    # Verificar endereço do usuário
    print("verificando endereço")
    address = get_object_or_404(user_address, user_id=request.user, address_id=request.data["user_address"])
    if not address:
        return Response({"message": "Endereço não encontrado"}, status=400)
    cart = get_object_or_404(Cart, user_id=request.user, is_active=True)
    cart.is_active = False
    cart.status = Cart.Status.Confirmed
    order = Order.objects.filter(cart=cart).first()
    cart_item = CartItem.objects.filter(cart=cart)
    if order is None:
        total = 0
        for item in cart_item:
            total += item.product.price * item.quantity
        serializer = OrderSerializer(data=request.data, context={"cart": cart, "total": total})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        order = get_object_or_404(Order, cart=cart)
    items = []
    for item in cart_item:
        item_data = dict(order=order.order_id, cart_item=item.id, total=(item.quantity*item.product.price))
        items.append(item_data)
    item_serializer = OrderItemSerializer(data=items, many=True)
    if not item_serializer.is_valid():
        return Response(item_serializer.errors, status=400)
    for item in cart_item:
        item.product.amount -= item.quantity
        item.product.reserved -= item.quantity
    order.status = Order.Status.Finished
    for item in cart_item:
        item.product.save()
    item_serializer.save()
    order.save()
    cart.save()
    return Response({"message": "Compra confirmada!"}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProductInCart(request):
    cart = get_object_or_404(Cart, user_id=request.user, is_active=True)
    cart_item = CartItem.objects.filter(cart=cart)
    products = []
    for item in cart_item:
        products.append(item.product)
    serializer = ProductSerializer(products, many=True)
    data = serializer.data
    for i in range(len(data)):
        data[i]["quantity"] = cart_item[i].quantity
    return Response(data, status=200)