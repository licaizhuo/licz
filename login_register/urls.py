from django.urls import path

from login_register import views

urlpatterns = [
    path("user/", views.UserLoginViewSet.as_view({"post": "user_login"})),
    path("sr/", views.UserGetRegisterViewSet.as_view({'get': 'list', "post": "user_register"})),
]
