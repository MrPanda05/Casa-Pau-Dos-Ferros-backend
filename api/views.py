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
        return Response({"message": "User registered!"}, status=201)
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
    return Response({"message": "Invalid credentials!"}, status=400)


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
    return Response({"message": "User logged out!"}, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_add_address(request):
    serializer = AddressSerializer(data=request.data)
    serializer.context['request'] = request
    if(serializer.is_valid()):
        serializer.save()
        return Response({"message": "Address set!"}, status=200)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated&IsAdminUser])
def staff_register(request):
    serializer = StaffUserSerializer(data=request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({"message": "Staff user registered!"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated&IsAdminUser])
def staff_Get(request):
    usermail = request.data["email"]
    UserAdmin = User.objects.filter(email=usermail).first()
    if(UserAdmin is None):
        return Response({"message": "User does not exist"}, status=400)
    isAdmin = UserAdmin.is_staff
    if(isAdmin):
        return Response({"message": "User is staff"}, status=200)
    else:
        return Response({"message": "User is not staff"}, status=200)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated&IsAdminUser])
def staff_Update(request):
    usermail = request.data["email"]
    UserAdmin = User.objects.filter(email=usermail).first()
    if(UserAdmin is None):
        return Response({"message": "User does not exist"}, status=400)
    isAdmin = UserAdmin.is_staff
    if(isAdmin):
        return Response({"message": "already admin"}, status=200)
    else:
        UserAdmin.is_staff = True
        UserAdmin.save()
        return Response({"message": "is now admin"}, status=200)
    

    
@api_view(["POST"])
@permission_classes([IsAuthenticated&IsAdminUser])
def staff_Delete(request):
    usermail = request.data["email"]
    UserAdmin = User.objects.filter(email=usermail).first()
    if(UserAdmin is None):
        return Response({"message": "User does not exist"}, status=400)
    isAdmin = UserAdmin.is_staff
    if(not isAdmin):
        return Response({"message": "already not admin"}, status=200)
    else:
        UserAdmin.is_staff = False
        UserAdmin.save()
        return Response({"message": "is now a peasent"}, status=200)


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
    return Response('No products found', status=404)