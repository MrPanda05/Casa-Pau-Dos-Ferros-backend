from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializer import *
from .models import User

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
            "userId": user.id
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
    user = User.objects.get(username=request.user)
    data = {"user_id": user.id, "cep": request.data["cep"], "country": request.data["country"], "state": request.data["state"], "city": request.data["city"], "neighborhood": request.data["neighborhood"], "street": request.data["street"], "number": request.data["number"], "complement": request.data["complement"]}
    serializer = AddressSerializer(data=data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({"message": "Address not set!"}, status=200)
    return Response(serializer.errors, status=400)