from django.db import models
from players.models import Player
from datetime import timedelta
from game_engine.enums import BoardType

four_by_four = [
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-'],
    ['-', '-', '-', '-'],
]

five_by_five = [
    ['-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-'],
]

class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="player", blank=True, null=True)
    board = models.JSONField(default=four_by_four)
    board_type = models.CharField(max_length=100, choices=BoardType.choices, default=BoardType.FOUR_BY_FOUR)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="winner", blank=True)
    duration = models.DurationField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "GAME"
        verbose_name_plural = "GAMES"