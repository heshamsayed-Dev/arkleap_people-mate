from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employee.models.company_model import Company
from employee.serializers.company_serializer import CompanySerializer
from django.http import Http404, QueryDict
from datetime import datetime

class CompanyAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                company = self.get_company_by_pk(pk)
                serializer = CompanySerializer(company)
            else:
                companies = Company.objects.all()
                serializer = CompanySerializer(companies, many=True)
            return Response(serializer.data)

        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            company=self.get_company_by_pk(pk)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(request.data)
            query_dict['updated_at'] = datetime.now()
            serializer = CompanySerializer(company, data=query_dict)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            company=self.get_company_by_pk(pk)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(request.data)
            query_dict['updated_at'] = datetime.now()
            serializer = CompanySerializer(company, data=query_dict, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            company=self.get_company_by_pk(pk)
            company.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)    

    def get_company_by_pk(self,pk):
        company = Company.objects.filter(pk=pk).first()
        if not company:
            raise Http404('Company not found')
        return company    
