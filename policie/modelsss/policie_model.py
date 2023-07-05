# from django.db import models
# from employee.models.company_model import Company
# from datetime import date
# from .common_model import CommonModel
# from employee.models.position_model import Position


# class Policy(CommonModel):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_policies")
#     working_hours = models.IntegerField()
#     start_of_working_hours = models.TimeField()
#     end_of_working_hours = models.TimeField()
#     start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
#     end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)


# class PositionPolicy(CommonModel):
#     policy = models.ForeignKey(Policy,on_delete=models.CASCADE,)
#     position = models.ForeignKey(Position, on_delete=models.CASCADE)
#     start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
#     end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
