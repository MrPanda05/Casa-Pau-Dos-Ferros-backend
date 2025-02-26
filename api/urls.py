from django.urls import path
from .views import *

urlpatterns = [
    path("hello/", hello_world),
    path("register/", user_register),
    path("login/", user_login),
    path("logout/", user_logout),
    path("address/", user_add_address),
    path("staff/", staff_register),
    path("staff/get", staff_Get),
    path("staff/update", staff_Update),
    path("staff/delete", staff_Delete),
    path("product/<int:category>", productByCategory),
    path("confirm/", confirmCart),
    #path("image/", user_image_update)
]