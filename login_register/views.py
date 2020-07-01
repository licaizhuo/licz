from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status

from app.models import User
from login_register.serializers import UserModelSerializer
from utils.response import MyResponse


class UserLoginViewSet(viewsets.ViewSet):
    def user_login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get("password")
        user = User.objects.filter(username=username, password=password)
        if user:
            return MyResponse(data_message="登入成功")
        return MyResponse(data_message="登入失败")


class UserGetRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserModelSerializer

    def user_register(self, request, *args, **kwargs):
        user = self.create(request, *args, **kwargs)
        return MyResponse(status.HTTP_201_CREATED, data_message="创建用户成功", results=user.data)
