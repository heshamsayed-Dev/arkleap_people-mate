from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employee.models.company_branch_model import CompanyBranch
from employee.serializers.company_branch_serializer import CompanyBranchSerializer
from django.http import Http404, QueryDict
from datetime import datetime

class CompanyBranchAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk:
                branch = self.get_branch_by_pk(pk)
                serializer = CompanyBranchSerializer(branch)
            else:
                branches = CompanyBranch.objects.all()
                serializer = CompanyBranchSerializer(branches, many=True)
            return Response(serializer.data)

        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CompanyBranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            branch=self.get_branch_by_pk(pk)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(request.data)
            query_dict['updated_at'] = datetime.now()
            serializer = CompanyBranchSerializer(branch, data=query_dict)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            branch=self.get_branch_by_pk(pk)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(request.data)
            query_dict['updated_at'] = datetime.now()
            serializer = CompanyBranchSerializer(branch, data=query_dict, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            branch=self.get_branch_by_pk(pk)
            branch.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404 as e:
            return Response({'message': str(e)}, status=status.HTTP_404_NOT_FOUND)    

    def get_branch_by_pk(self,pk):
        branch = CompanyBranch.objects.filter(pk=pk).first()
        if not branch:
            raise Http404('Branch not found')
        return branch    
