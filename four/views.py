from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, \
    ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.views import APIView
from four.serializers import BookModelSerializer
from three.models import Book
from utils.response import MyResponse


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_list = Book.objects.filter(is_delete=False)
        data_ser = BookModelSerializer(book_list, many=True).data

        return MyResponse(results=data_ser)

    def post(self, request, *args, **kwargs):
        data_ser = BookModelSerializer(data=request.data, context={'request': request})
        data_ser.is_valid(raise_exception=True)
        data = data_ser.save()
        return MyResponse(results=BookModelSerializer(data).data)


# view generics mixins viewsets
# generics：工具视图，提供了许多内置的工具
# mixins: 五大工具类，分别提供不同的操作
# viewsets`：视图集

class BookGenericAPIView(GenericAPIView,
                         ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    # TODO 只是继承GenericAPIView时
    # def get(self, request, *args, **kwargs):
    #
    #     if kwargs.get(self.lookup_field):
    #         book_info = self.get_object()
    #         many = False
    #     else:
    #         book_info = self.get_queryset()
    #         many = True
    #     data_ser = self.get_serializer(book_info, many=many).data
    #     return MyResponse(results=data_ser)

    # TODO 继承GenericAPIView和ListModelMixin时
    # 五大工具类之--ListModelMixin查询全部self.list
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # TODO 继承GenericAPIView、ListModelMixin、RetrieveModelMixin时
    # 五大工具类之--ListModelMixin查询全部self.list
    # 五大工具类之--RetrieveModelMixin查询单个self.retrieve
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    # TODO 继承GenericAPIView、CreateModelMixin时
    # 五大工具类之--CreateModelMixin时创建单个self.create
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # TODO 继承GenericAPIView、UpdateModelMixin
    # 五大工具类之--UpdateModelMixin单个整体修改self.update
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # TODO 继承GenericAPIView、UpdateModelMixin
    # 五大工具类之--UpdateModelMixin单个局部修改self.partial_update
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # TODO 继承GenericAPIView、DestroyModelMixin
    # 五大工具类之--DestroyModelMixin单个删除self.delete
    def delete(self, request, *args, **kwargs):
        a = self.destroy(request, *args, **kwargs)
        print(a)
        return MyResponse(http_status=status.HTTP_204_NO_CONTENT)


# class BookGenericNine(CreateAPIView):
#     # CreateAPIView(mixins.CreateModelMixin,GenericAPIView)
#     # 用于便捷创建
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer

# class BookGenericNine(ListAPIView):
#     # ListAPIView(mixins.ListModelMixin,GenericAPIView)
#     # 用于查询全部
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer

# class BookGenericNine(CreateAPIView):
#     # RetrieveAPIView(mixins.RetrieveModelMixin, GenericAPIView)
#     # 用于查询单个
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer
#     lookup_field = "id"

# class BookGenericNine(DestroyAPIView):
#     # DestroyAPIView(mixins.DestroyModelMixin,GenericAPIView)
#     # 用于删除单个
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer
#     lookup_field = "id"

# class BookGenericNine(UpdateAPIView):
#     # UpdateAPIView(mixins.UpdateModelMixin,GenericAPIView)
#     # 可以进行单个局部更新和单个整体更新
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer
#     lookup_field = "id"

# class BookGenericNine(ListCreateAPIView):
#     # ListCreateAPIView(mixins.ListModelMixin,mixins.CreateModelMixin,GenericAPIView)
#     # 可以查询全部和增加单个
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer
#     lookup_field = "id"

# class BookGenericNine(RetrieveUpdateAPIView):
#     # RetrieveUpdateAPIView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,GenericAPIView)
#     # 可以查询单个和单个局部更新和单个整体更新
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer
#     lookup_field = "id"

# class BookGenericNine(RetrieveUpdateDestroyAPIView):
#     # RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,GenericAPIView)
#     # 可以查询单个和单个局部更新和单个整体更新和删除单个
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer
#     lookup_field = "id"
# class BookListAPIVIew(generics.ListCreateAPIView, generics.DestroyAPIView):
#     queryset = Book.objects.filter(is_delete=False)
#     serializer_class = BookModelSerializer
#     lookup_field = "id"


class BookGenericViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    def user_login(self, request, *args, **kwargs):
        # 可以在此方法中完成用户登录的逻辑
        return self.retrieve(request, *args, **kwargs)

    def get_user_count(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
