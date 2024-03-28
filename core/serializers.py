from djoser.serializers import UserCreateSerializer as BaseUserCreateSerialzier
from djoser.serializers import UserSerializer as BaseUserSerialzier


class UserCreateSerializer(BaseUserCreateSerialzier):
    class Meta(BaseUserCreateSerialzier.Meta):
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        ]


class UserSerializer(BaseUserSerialzier):
    class Meta(BaseUserSerialzier.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]
