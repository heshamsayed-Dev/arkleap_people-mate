# from datetime import datetime
from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.policy_model import Policy
from ..serializers.policy_serializer import policySerializer


class PolicyViewSet(viewsets.ViewSet):
    queryset = Policy.objects.all()
    model = Policy
    serializer_class = policySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.queryset.order_by("-created_at")
        paginator = self.pagination_class()
        objects = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(objects, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        try:
            if request.method == "POST":
                user = request.user

                serializer = self.serializer_class(data=request.data, context={"user": user})
                if serializer.is_valid():
                    serializer.save()
                    return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"success": True, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = request.user
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance, request.data, context={"user": user})
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"success": True, "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
            return Response(data="no policy with this id", status=status.HTTP_400_BAD_REQUEST)
        except self.model.MultipleObjectsReturned:
            return Response(data="there is more than one obj with this id", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.serializer_class(instance)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
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
