from django.urls import path
from .views import *

urlpatterns = [
    path("hello/", hello_world),
    path("register/", user_register),
    path("login/", user_login),
    #path("logout/", user_logout),
    #path("profile/", user_profile),
    #path("image/", user_image_update)
]