from djoser.serializers import UserCreateSerializer as BaseUserCreateSerialzier


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
