# from datetime import date
from django.core.paginator import Paginator
from rest_framework import status, viewsets
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from people_mate.users.models import User
from datetime import datetime
from ..models.policy_model import Policy
from ..serializers.policy_serializer import policySerializer


class PolicyViewSet(viewsets.ViewSet):
    queryset = Policy.objects.all()
    model = Policy
    serializer_class = policySerializer
    pagination_class = Paginator


    # permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.queryset.order_by("-created_at")
        serializer = self.serializer_class(queryset, many=True)
        data = {"success": True, "data": serializer.data,"count":queryset.count()}
        return Response(data, status=status.HTTP_200_OK)
    



    def create(self, request):
        try:
            if request.method == "POST":
                user = User.objects.get(id=1)
                serialezer = self.serializer_class(data=request.data, context={"user": user})
                if serialezer.is_valid():
                    serialezer.save()
                    data = {"success": True, "data": serialezer.data}    
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    data = {"success": True, "data": serialezer.errors}    
                    return Response(data ,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = User.objects.get(id=1)

        try:
            instance = self.queryset.get(pk=pk)
            serialezer = self.serializer_class(instance, request.data, context={"user": user})
            if serialezer.is_valid():
                serialezer.save()
                data = {"success": True, "data": serialezer.data}    
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"success": True, "data": serialezer.errors}    
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
            return Response(data="no policy with this id", status=status.HTTP_400_BAD_REQUEST)
        except self.model.MultipleObjectsReturned:
            return Response(data="there is more than one obj with this id", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serialezer = self.serializer_class(instance)
            data = {"success": True, "data": serialezer.data}    
            return Response(data, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response(data="no policy with this id", status=status.HTTP_400_BAD_REQUEST)
        except self.model.MultipleObjectsReturned:
            return Response(data="there is more than one obj with this id", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            instance.delete()
            return Response("policy deleted", status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response(data="no policy  with this id", status=status.HTTP_404_NOT_FOUND)
        except self.model.MultipleObjectsReturned:
            return Response(data="there is more than one obj with this id", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)
