from django.apps import apps
from django.http import Http404


def get_model_by_pk(model_name, pk):
    model = apps.get_model("attendance", model_name)
    obj = model.objects.filter(pk=pk).first()
    if not obj:
        raise Http404(f"{model_name} not found")
    return obj


def calculate_checkout_time(details):
    checkout = details.first().check_out
    for det in details:
        if det.check_out > checkout:
            checkout = det.check_out

    return checkout


def calculate_worked_hours(details):
    worked_hours = 0
    for det in details:
        worked_hours += (det.check_out - det.check_in).total_seconds() / 3600

    return worked_hours
