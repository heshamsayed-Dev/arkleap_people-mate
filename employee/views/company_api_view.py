from datetime import datetime

from django.http import Http404, QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from employee.models.company_model import Company
from employee.serializers.company_serializer import CompanySerializer

from .utils import CustomPaginator, get_model_by_pk


class CompanyAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                company = get_model_by_pk("Company", pk)
                serializer = CompanySerializer(company)
            else:
                companies = request.user.companies().filter(end_date__lte=datetime.today().date())
                paginator = CustomPaginator(1)
                paginated_companies = paginator.paginate_queryset(companies, request)
                serializer = CompanySerializer(paginated_companies, many=True)
                return paginator.get_paginated_response(serializer.data)

        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            company = self.perform_create(serializer)
            request.user.companies.add(company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            company = get_model_by_pk("Company", pk)
            query_dict = QueryDict("", mutable=True)
            query_dict.update(request.data)
            query_dict["updated_at"] = datetime.now()
            serializer = CompanySerializer(company, data=query_dict)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            company = get_model_by_pk("Company", pk)
            query_dict = QueryDict("", mutable=True)
            query_dict.update(request.data)
            query_dict["updated_at"] = datetime.now()
            serializer = CompanySerializer(company, data=query_dict, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            company = get_model_by_pk("Company", pk)
            if not company.employees.exists() or company.departments.exists():
                company.end_date = datetime.today().date()
                company.save()
                return Response(data={"message": "Company deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    data={"message": "Your enterprise is already active and cannote be removed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Http404 as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
