from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User name is taken")
        else:
            return username

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"].lower(),
        )
        user.set_password(validated_data["password"])
        user.save()

        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("account not found")
        else:
            return username

    def get_jwt_token(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            return {
                "message": "Invalid credentials",
                "status": False,
            }
        else:
            refresh = RefreshToken.for_user(user)
            return {
                "message": "Login Success",
                "status": True,
                "data": {
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
            }
