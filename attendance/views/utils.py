from django.apps import apps
from django.http import Http404


def get_model_by_pk(model_name, pk):
    model = apps.get_model("attendance", model_name)
    obj = model.objects.filter(pk=pk).first()
    if not obj:
        raise Http404(f"{model_name} not found")
    return obj
