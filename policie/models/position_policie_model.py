from django.db import models

from employee.models.position_model import Position

from .common_model import CommonModel
from .policie_model import Policie


class PositionPolicie(CommonModel):
    Policie = models.ForeignKey(
        Policie,
        on_delete=models.CASCADE,
    )
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
