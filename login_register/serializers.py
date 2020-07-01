from rest_framework import serializers

from app.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "gender")
        extra_kwargs = {
            "username": {
                "required": True,
                "error_messages": {
                    "required": "用户名是必填项"
                }
            },
            "password": {
                "required": True,
                "error_messages": {
                    "required": "密码名是必填项"
                }
            },
            "gender": {
                "read_only": True
            }
        }
