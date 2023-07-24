from django.contrib.auth import get_user_model
from rest_framework import serializers

# import re
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm", "avatar"]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError({"details": "passwords didnt match"})

        return data

    def create(self, validated_data, **kwargs):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user

    # def validate_email(self,value):
    #     if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
    #         raise serializers.ValidationError("Invalid email address that follows this example User@host.com")
    #     return value


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
