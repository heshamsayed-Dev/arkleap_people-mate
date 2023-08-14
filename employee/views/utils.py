from django.apps import apps
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def get_model_by_pk(model_name, pk):
    model = apps.get_model("employee", model_name)
    obj = model.objects.filter(pk=pk).first()
    if not obj:
        raise Http404(f"{model_name} not found")
    return obj


# from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    def __init__(self, page_size=10, max_page_size=100):
        self.page_size = page_size
        self.max_page_size = max_page_size

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        )
