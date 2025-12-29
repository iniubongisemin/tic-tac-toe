from django.db import models
from django.utils.translation import gettext_lazy as _

class BoardType(models.TextChoices):
    FOUR_BY_FOUR = _("4X4"), "4X4"
    FIVE_BY_FIVE = _("5X5"), "5X5"

    