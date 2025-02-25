from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'address', AddressViewSet, basename='address')
router.register(r'users', UserViewSet)
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'product_category', ProductCategoryViewSet)
router.register(r'cart', CartViewSet)
router.register(r'cart_item', CartItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("", include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]