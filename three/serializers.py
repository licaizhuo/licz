from rest_framework import serializers, exceptions
from rest_framework.serializers import ListSerializer

from three.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name", "pic")


class BookModelSerializer(serializers.ModelSerializer):
    publish = PressModelSerializer()

    class Meta:
        model = Book
        # fields = ("book_name", "price")
        # fields = "__all__"
        # exclude = ("is_delete", 'status')
        # depth = 1
        fields = ("book_name", "price", "pic", "publish")


class BookDeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")

    def validate_book_name(self, value):
        if "卧槽" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

    def validate(self, attrs):
        p = attrs.get('price', 0.1)
        if p <= 0:
            raise exceptions.ValidationError("请填写一个正确的价格")
        return attrs


class BookListSerializer(ListSerializer):

    def update(self, instance, validated_data):
        return [
            self.child.update(obj, validated_data[index]) for index, obj in enumerate(instance)
        ]


class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors", "pic")
        list_serializer_class = BookListSerializer
        extra_kwargs = {
            "book_name": {
                "required": True,
                "error_messages": {
                    "required": "图书名是必填项"
                }
            },
            "pic": {
                "read_only": True
            }
        }

    def validate_book_name(self, value):
        if "卧槽" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

    def validate(self, attrs):
        p = attrs.get('price', 0.1)
        if p <= 0:
            raise exceptions.ValidationError("请填写一个正确的价格")
        return attrs
