#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicTacToe.settings')
django.setup()

from game_engine.game_play import Play

if __name__ == '__main__':
    game = Play()
    game.start()
