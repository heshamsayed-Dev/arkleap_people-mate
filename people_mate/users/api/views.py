from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action 
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

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

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        serializer=UserSerializer(data=request.data,context={'request': request})
        if (serializer.is_valid()):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_permissions(self):
        if self.action == 'signup':
            return [AllowAny()]
        else:
            return super().get_permissions()


    @action(detail=False)
    def signout(self,request):
        # print(request.user.password)
        # request.user.auth_token.delete()
        return Response(data={"message": "you are successfully logged out"}, status=status.HTTP_200_OK)            
