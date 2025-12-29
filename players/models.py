from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import PlayerManager

class Player(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    games_played = models.PositiveBigIntegerField(default=0)
    games_won = models.PositiveBigIntegerField(default=0)
    games_drawn = models.PositiveBigIntegerField(default=0)
    date_joined = models.DateField(auto_now_add=True)

    objects = PlayerManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "PLAYER"
        verbose_name_plural = "PLAYERS"
