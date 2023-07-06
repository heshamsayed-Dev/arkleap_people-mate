from datetime import date

from django.db.models import Q
from rest_framework import status, viewsets

# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.paginator import Pagination

from ..models.policy_model import Policy
from ..serializers.policy_serializer import policySerializer


class PolicyViewSet(viewsets.ViewSet):
    queryset = Policy.objects.all()
    model = Policy
    serializer_class = policySerializer
    pagination_class = Pagination

    # permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = self.queryset.filter(Q(end_date__gte=date.today()) | Q(end_date__isnull=True)).order_by(
            "-created_at"
        )
        serializer = self.serializer_class(queryset, many=True)
        # results = self.pagination_class(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    #  count=queryset.count()

    def create(self, request):
        try:
            if request.method == "POST":
                serialezer = self.get_serializer(data=request.data, context={"user": request.user})
                if serialezer.is_valid():
                    serialezer.save()
                    return Response(data=serialezer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(data=serialezer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serialezer = self.get_serializer(instance, request.data)
            if serialezer.is_valid():
                serialezer.save()
                return Response(data=serialezer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serialezer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
            return Response(data="no policie with this id", status=status.HTTP_400_BAD_REQUEST)
        except self.model.MultipleObjectsReturned:
            return Response(data="there is more than one obj with this id", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            serialezer = self.get_serializer(instance)
            return Response(data=serialezer.data, status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response(data="no policie with this id", status=status.HTTP_400_BAD_REQUEST)
        except self.model.MultipleObjectsReturned:
            return Response(data="there is more than one obj with this id", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            instance = self.queryset.get(pk=pk)
            instance.delete()
            return Response("policie deleted", status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response(data="no policie with this id", status=status.HTTP_404_NOT_FOUND)
        except self.model.MultipleObjectsReturned:
            return Response(data="there is more than one obj with this id", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"error:{e}, please connect to admin"}, status=status.HTTP_400_BAD_REQUEST)
