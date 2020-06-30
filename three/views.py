from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from three.models import Book
from three.serializers import BookModelSerializer, BookDeModelSerializer, BookModelSerializerV2


class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            book_id = kwargs.get('id')
            if book_id:
                book_obj = Book.objects.get(pk=book_id)
                book_ser = BookModelSerializer(book_obj)
                # print(book_ser)
                book_info = book_ser.data
                # print(book_ser)
                message = "单个图书查询成功了"

            else:
                book_list = Book.objects.all()
                book_list_ser = BookModelSerializer(book_list, many=True)
                book_info = book_list_ser.data
                message = "查询所有图书成功"
            return Response({
                "status": status.HTTP_200_OK,
                "message": message,
                "results": book_info
            })
        except:
            raise exceptions.NotFound("查询图书失败")

    def post(self, request, *args, **kwargs):
        try:
            book_data = request.data
            book_ser = BookDeModelSerializer(data=book_data)
            book_ser.is_valid(raise_exception=True)
            with transaction.atomic():
                book_obj = book_ser.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "添加图书成功",
                    "result": BookModelSerializer(book_obj).data
                })
        except:
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                 "message": "图书添加失败"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)


class BookAPIViewV1(APIView):

    def get(self, request, *args, **kwargs):
        try:
            book_id = kwargs.get('id')
            if book_id:
                book_obj = Book.objects.filter(pk=book_id, is_delete=False)
                if book_obj:
                    book_ser = BookModelSerializer(book_obj)
                    book_info = book_ser.data
                    message = "单个图书查询成功了"
                else:
                    raise
            else:
                book_list = Book.objects.filter(is_delete=False)
                book_list_ser = BookModelSerializer(book_list, many=True)
                book_info = book_list_ser.data
                message = "查询所有图书成功"
            return Response({
                "status": status.HTTP_200_OK,
                "message": message,
                "results": book_info
            })
        except:
            raise exceptions.NotFound("查询图书失败")

    def post(self, request, *args, **kwargs):
        try:
            book_data = request.data
            if isinstance(book_data, dict):
                many = False
            elif isinstance(book_data, list):
                many = True
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "请求参数格式有误",
                })
            book_ser = BookDeModelSerializer(data=book_data, many=many)
            book_ser.is_valid(raise_exception=True)
            with transaction.atomic():
                book_obj = book_ser.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "添加图书成功",
                    "result": BookModelSerializer(book_obj, many=many).data
                })
        except:
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                 "message": "图书添加失败"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或图书不存在"
        })

    def put(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        book_ser = BookDeModelSerializer(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializer(book_obj).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        book_ser = BookDeModelSerializer(data=request_data, instance=book_obj, partial=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializer(book_obj).data
        })


class BookAPIViewV2(APIView):

    def get(self, request, *args, **kwargs):
        try:
            book_id = kwargs.get('id')
            if book_id:
                book_obj = Book.objects.filter(pk=book_id, is_delete=False)
                if book_obj:
                    book_ser = BookModelSerializerV2(book_obj)
                    book_info = book_ser.data
                    message = "单个图书查询成功了"
                else:
                    raise
            else:
                book_list = Book.objects.filter(is_delete=False)
                book_list_ser = BookModelSerializerV2(book_list, many=True)
                book_info = book_list_ser.data
                message = "查询所有图书成功"
            return Response({
                "status": status.HTTP_200_OK,
                "message": message,
                "results": book_info
            })
        except:
            raise exceptions.NotFound("查询图书失败")

    def post(self, request, *args, **kwargs):
        try:
            book_data = request.data
            if isinstance(book_data, dict):
                many = False
            elif isinstance(book_data, list):
                many = True
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "请求参数格式有误",
                })
            book_ser = BookModelSerializerV2(data=book_data, many=many)
            book_ser.is_valid(raise_exception=True)
            with transaction.atomic():
                book_obj = book_ser.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "添加图书成功",
                    "result": BookModelSerializerV2(book_obj, many=many).data
                })
        except:
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                 "message": "图书添加失败"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或图书不存在"
        })

    def put(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializerV2(book_obj).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializerV2(book_obj).data
        })
