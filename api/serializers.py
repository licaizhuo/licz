from rest_framework import serializers

from api.models import Employee
from drf_study import settings


class EmployeeSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        return obj.get_gender_display()

    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, str(obj.pic))


class EmployeeDeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=10,
        min_length=2,
    )
    password = serializers.CharField(required=False)
    phone = serializers.CharField()

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)
