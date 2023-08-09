from django.apps import apps
from django.http import Http404
from rest_framework.pagination import PageNumberPagination


def get_model_by_pk(model_name, pk):
    model = apps.get_model("employee", model_name)
    obj = model.objects.filter(pk=pk).first()
    if not obj:
        raise Http404(f"{model_name} not found")
    return obj


class CustomPaginator(PageNumberPagination):
    def __init__(self, page_size=10):
        self.page_size = page_size
