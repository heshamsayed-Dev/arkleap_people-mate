# from datetime import date

# from django.db import models

# from employee.models.position_model import Position

# from .common_model import CommonModel
# from .policy_model import Policy


# class PositionPolicy(CommonModel):
#     policy = models.ForeignKey(
#         Policy,
#         on_delete=models.CASCADE,
#     )
#     position = models.ForeignKey(Position, on_delete=models.CASCADE)
#     start_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today)
#     end_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
