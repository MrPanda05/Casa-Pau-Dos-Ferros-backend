from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# address_list = AddressViewSet.as_view({
#     'get': 'list'
# })
# address_detail = AddressViewSet.as_view({
#     'get': 'retrieve',
# })

router = DefaultRouter()
router.register(r'address', AddressViewSet, basename='address')
router.register(r'users', UserViewSet)
router.register(r'staff', StaffViewSet, basename='staff')


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("", include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]