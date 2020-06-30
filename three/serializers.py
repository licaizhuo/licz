from rest_framework import serializers, exceptions

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


class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors", "pic")
        extra_kwargs = {
            "book_name": {
                "required": True,
                "error_messages": {
                    "required": "图书名是必填项"
                }
            },
            "publish": {
                "write_only": True
            },
            "authors": {
                "write_only": True
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
