from django.core.management.base import BaseCommand
from game_engine.game_play import Play


class Command(BaseCommand):
    help = 'Start a Tic Tac Toe game'

    def handle(self, *args, **options):
        game = Play()
        game.start()
