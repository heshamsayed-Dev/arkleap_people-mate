import pyotp
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from employee.models.company_model import Company
from people_mate.users.signals import generate_otp_qrcode, generate_user_secret_key, send_mail_to_user

from .serializers import ResetPasswordSerializer, SignInSerializer, UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    def verify_otp(self, user, otp):
        totp = pyotp.TOTP(user.otp_secret, interval=30)
        if totp.verify(otp):
            return True
        else:
            return False

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["POST"])
    def signup(self, request):
        serializer = UserSerializer(
            data=request.data, context={"request": request, "user_companies": request.user.companies}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "User created successfully wait for admin approval"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def sign_in(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=request.data["email"])
                if user.check_password(request.data["password"]):
                    if not self.verify_otp(user, request.data["otp"]):
                        refresh = RefreshToken.for_user(user)
                        return Response(
                            data={
                                "access": str(refresh.access_token),
                                "username": user.username,
                                "user type": user.role,
                                "avatar": "people_mate/people_mate/media/" + str(user.avatar),
                            },
                            status=200,
                        )
                    else:
                        return Response(
                            data={"message": "Incorrect OTP"},
                            status=status.HTTP_403_FORBIDDEN,
                        )
                else:
                    return Response(
                        data={
                            "message": "invalid email or password",
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except User.DoesNotExist:
                return Response(data={"message": "there is no such email"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # checks if correct mail is submitted will send mail with the newly generated qr code to user
    @action(detail=False, methods=["POST"])
    def reset_password_send_email(self, request):
        if request.data.get("email"):
            try:
                user = User.objects.get(email=request.data["email"])
                generate_user_secret_key(user)
                image_stream = generate_otp_qrcode(user)
                send_mail_to_user(request.data["email"], image_stream)
                return Response(
                    data={"user": user.id, "message": "Comfirmation mail has been sent to your Email "},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(data={"message": "there is no such email"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={"message": "Email must be sent"}, status=status.HTTP_401_UNAUTHORIZED)

    # validates otp sent by user
    @action(detail=False, methods=["POST"])
    def reset_password_validate_otp(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if request.data.get("otp"):
                if self.verify_otp(user, request.data["otp"]):
                    return Response(data={"user": user.id, "message": "Correct OTP"}, status=status.HTTP_200_OK)
                else:
                    return Response(data={"message": "Incorrect OTP"}, status=status.HTTP_403_FORBIDDEN)

            else:
                return Response(data={"message": "OTP must be sent"}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response(data={"message": "there is no user with such ID"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["POST"])
    def reset_password(self, request, pk):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(id=pk)
                user.password = make_password(request.data["password"])
                user.save()
                return Response(data={"message": "password has been successfully changed"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data={"message": "there is no user with such ID"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["Patch"])
    def update_user(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(
                user, data=request.data, partial=True, context={"user_companies": request.user.companies}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(data={"message": "User updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(data={"message": "there is no user with such ID"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=["post"])
    def activate_company(self, request, pk):
        try:
            company = request.user.companies.get(id=pk)
            request.user.company = company
            request.user.save()
            return Response(data={"message": "Company successfully activated"}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response(data={"message": "you cant activate this company"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def signout(self, request):
        # print(request.user.password)
        # request.user.auth_token.delete()
        return Response(data={"message": "you are successfully logged out"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in (
            # "signup",
            "sign_in",
            "reset_password_send_email",
            "reset_password_validate_otp",
            "reset_password",
        ):
            return [AllowAny()]
        else:
            return super().get_permissions()
