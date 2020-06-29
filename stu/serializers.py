from rest_framework import serializers

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
    phone = serializers.CharField(
        max_length=11,
        min_length=11,
    )

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
