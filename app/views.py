from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import settings


# Create your views here.
# @csrf_protect 为某个视图增加csrf验证
@csrf_exempt  # 免除csrf验证
def user(request):
    if request.method == "GET":
        print("查询")
        return HttpResponse("11111")

    elif request.method == "POST":
        print("添加")
        return HttpResponse("22222")

    elif request.method == "PUT":
        print("修改")
        return HttpResponse("333333")

    elif request.method == "DELETE":
        print("删除")
        return HttpResponse("44444")


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    def get(self, request, *args, **kwargs):
        """
        :param request: 用户id
        :return: 查询的用户信息
        """
        # 获取用户的id，并且不能使用GET获取，因为不是参数URL不是拼接参数，而是一个用户对应一个url
        user_id = kwargs.get('id')
        if user_id:
            user_val = User.objects.filter(pk=user_id).values("username", "password", "gender")
            if user_val:
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": user_val.first(),
                })
        else:
            user_list = User.objects.filter().values("username", "password", "gender")
            if user_list:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_list),
                })
        return JsonResponse({
            "status": 500,
            "message": "查询失败",
        })

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            user_obj = User.objects.create(username=username, password=pwd)
            return JsonResponse({
                "status": 201,
                "message": "创建用户成功",
                "results": {"username": user_obj.username, "gender": user_obj.gender}
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # user_id = request.GET.get("id")
        # print(user_id)
        # user_id = request.query_params.get('id')
        user_id = kwargs.get('id')
        user_val = User.objects.get(pk=user_id)
        # if user_id:
        #     user_val = User.objects.filter(pk=user_id).values("username", "password", "gender")
        #     if user_val:
        #         return JsonResponse({
        #             "status": 200,
        #             "message": "查询单个用户成功",
        #             "results": user_val.first(),
        #         })
        # else:
        #     user_list = User.objects.filter().values("username", "password", "gender")
        #     if user_list:
        #         return JsonResponse({
        #             "status": 200,
        #             "message": "查询所有用户成功",
        #             "results": list(user_list),
        #         })
        return Response("DRF GET SUCCESS")

    def post(self, request, *args, **kwargs):
        try:
            # username = request.POST.get("username")
            username = request.data.get('username')
            pwd = request.POST.get("pwd")
            with transaction.atomic():
                user_obj = User.objects.create(username=username, password=pwd)
                return JsonResponse({
                    "status": 201,
                    "message": "创建用户成功",
                    "results": {"username": user_obj.username, "gender": user_obj.gender}
                })
        except:
            return JsonResponse({
                "status": 500,
                "message": "创建用户失败",
            })

    def put(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('id')
            username = request.POST.get("username")
            # username = request.data.get('username')
            pwd = request.data.get('pwd')
            # pwd = request.POST.get("pwd")
            gender = request.POST.get("gender")
            user_obj = User.objects.filter(pk=user_id)
            if user_id:
                with transaction.atomic():
                    user_obj = user_obj.first()
                    if username:
                        user_obj.username = username
                    if pwd:
                        user_obj.password = pwd
                    if gender:
                        user_obj.gender = gender
                    user_obj.save()
                    return JsonResponse({
                        "status": 201,
                        "message": "修改用户成功",
                        "results": {"username": user_obj.username, "gender": user_obj.gender}
                    })
        except:
            return JsonResponse({
                "status": 500,
                "message": "修改用户失败",
            })

    def delete(self, request, *args, **kwargs):
        try:
            # print(request.GET)
            # print(request.query_params)
            user_id = kwargs.get('id')
            user_obj = User.objects.filter(pk=user_id)
            if user_id:
                with transaction.atomic():
                    user_obj = user_obj.first()
                    username = user_obj.username
                    gender = user_obj.gender
                    user_obj.delete()
                    user_obj.save()
                    return JsonResponse({
                        "status": 201,
                        "message": "删除用户成功",
                        "results": {"username": username, "gender": gender}
                    })
        except:
            return JsonResponse({
                "status": 500,
                "message": "删除用户失败",
            })


class StudentAPIView(APIView):
    # 局部渲染
    # renderer_classes = (BrowsableAPIRenderer, JSONRenderer)
    # 局部解析器
    # parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response("访问成功-post")

    def get(self, request, *args, **kwargs):
        return Response("访问成功-get")
