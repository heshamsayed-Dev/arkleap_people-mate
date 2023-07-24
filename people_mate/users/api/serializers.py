import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

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

    def validate_password(self, value):
        # Define a regex pattern to match passwords with at least 8 characters,
        # one lowercase letter, one uppercase letter, one digit, and one special character.
        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{8,}$"

        # Check if the value matches the pattern.
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                """Password must be at least 8 characters long and contain at least one
lowercase letter, one uppercase letter, one digit, and one special character.""".replace(
                    "\n", " "
                )
            )

        return value


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)
