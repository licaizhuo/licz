from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from stu.models import Student
from stu.serializers import StudentSerializer, StudentDeSerializer


class StudentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        stu_id = kwargs.get("pk")
        if stu_id:
            stu_obj = Student.objects.get(pk=stu_id)
            stu_ser = StudentSerializer(stu_obj)
            data = stu_ser.data

            return Response({
                "status": 200,
                "msg": "查询单个学生成功",
                "results": data,
            })
        else:

            stu_list = Student.objects.all()

            stu_list_ser = StudentSerializer(stu_list, many=True)
            data = stu_list_ser.data
            return Response({
                "status": 200,
                "msg": "查询所有学生成功",
                "results": data,
            })

    def post(self, request, *args, **kwargs):

        stu_data = request.data

        if not isinstance(stu_data, dict) or stu_data == {}:
            return Response({
                "status": 501,
                "msg": "数据出现错误",
            })
        serializer = StudentDeSerializer(data=stu_data)
        if serializer.is_valid():
            stu_obj = serializer.save()
            # 将创建成功的用户实例返回到前端
            return Response({
                "status": 201,
                "msg": "学生添加成功",
                "results": StudentSerializer(stu_obj).data
            })
        else:
            return Response({
                "status": 501,
                "msg": "学生添加失败",
                "results": serializer.errors
            })
