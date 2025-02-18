from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404

from api.models import *
from api.serializer import *

class AddressViewSet(viewsets.ModelViewSet):
    queryset = user_address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = get_list_or_404(user_address, user_id=request.user.id)
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data)
    
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


class StaffViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = StaffUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]