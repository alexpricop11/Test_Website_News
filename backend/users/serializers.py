from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Users


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = Users
        fields = ["username", "email", "password"]

    @staticmethod
    def validate_username(value: str) -> str:
        if Users.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data: dict) -> Users:
        return Users.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, data: dict) -> dict:
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        data["user"] = user
        return data
