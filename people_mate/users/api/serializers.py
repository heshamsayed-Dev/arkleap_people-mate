import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_confirm", "avatar", "role", "companies", "company"]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError({"messages": "passwords didnt match"})

        return data

    def create(self, validated_data, **kwargs):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.companies.set(validated_data["companies"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_companies(self, value):
        if value:
            admin_companies_set = set(self.context.get("user_companies").values_list("id", flat=True))
            sent_companies = {int(company.id) for company in value}
            if not sent_companies.issubset(admin_companies_set):
                raise serializers.ValidationError("you cant give access to companies you dont have access to")
        return value

    def update(self, instance, validated_data):
        if validated_data.get("role"):
            instance.role = validated_data.get("role")
        if validated_data.get("username"):
            instance.username = validated_data.get("username")
        if validated_data.get("email"):
            instance.email = validated_data.get("email")
        if validated_data.get("companies"):
            instance.companies.set(validated_data.get("companies"))
        if validated_data.get("avatar"):
            instance.avatar = validated_data.get("avatar")

        instance.save()
        return instance

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
    otp = serializers.CharField(max_length=255, required=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, required=True)
    password_confirm = serializers.CharField(max_length=255, required=True)

    def validate(self, data):
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError({"message": "passwords didnt match"})

        return data

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
