from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignInSerializer, UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["POST"])
    def signup(self, request):
        serializer = UserSerializer(data=request.data, context={"request": request})
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
                    if user.is_active:
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
                            data={"message": "contact your admin to confirm your email first"},
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

    @action(detail=False)
    def signout(self, request):
        # print(request.user.password)
        # request.user.auth_token.delete()
        return Response(data={"message": "you are successfully logged out"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ("signup", "sign_in"):
            return [AllowAny()]
        else:
            return super().get_permissions()
