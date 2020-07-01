from rest_framework import serializers, exceptions

from three.models import Book, Press


class BookListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        return [
            self.child.update(obj, validated_data[index]) for index, obj in enumerate(instance)
        ]


class BookModelSerializer(serializers.ModelSerializer):
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
        # print("2222------>", self.context.get('request'))
        if "卧槽" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

    def validate(self, attrs):
        p = attrs.get('price', 0.1)
        # print('111')
        # print("1111------>", self.context.get('request'))

        if p <= 0:
            raise exceptions.ValidationError("请填写一个正确的价格")
        return attrs
