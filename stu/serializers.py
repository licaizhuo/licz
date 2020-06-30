from rest_framework import serializers, exceptions

from stu.models import Student


class StudentSerializer(serializers.Serializer):
    name = serializers.CharField()
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        return obj.get_gender_display()


class StudentDeSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=10,
        min_length=2,
    )
    phone = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        if len(phone) != 11:
            raise exceptions.ValidationError('请输入正确的手机号')
        return attrs

    def validate_name(self, value):
        if '我操' in value:
            raise exceptions.ValidationError("用户名包含敏感词")
        return value

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
