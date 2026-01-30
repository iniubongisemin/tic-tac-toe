from django.test import TestCase
from players.models import Player
from game_engine.models import Game
from game_engine.game_play import Play
import copy


class GamePlayTestCase(TestCase):
    def setUp(self):
        self.player = Player.objects.create_user(username='testuser', password='testpass')
        self.play = Play()
        self.play.player = self.player
        self.play.board_size = 4
        self.play.board = [['-' for _ in range(4)] for _ in range(4)]
    
    def test_make_move(self):
        """Test making a move on the board"""
        self.play.make_move(0, 0, 'X')
        self.assertEqual(self.play.board[0][0], 'X')
    
    def test_check_winner_row(self):
        """Test row win detection"""
        for i in range(4):
            self.play.board[0][i] = 'X'
        winner = self.play.check_winner()
        self.assertEqual(winner, 'X')
    
    def test_check_winner_column(self):
        """Test column win detection"""
        for i in range(4):
            self.play.board[i][0] = 'O'
        winner = self.play.check_winner()
        self.assertEqual(winner, 'O')
    
    def test_check_winner_diagonal(self):
        """Test diagonal win detection"""
        for i in range(4):
            self.play.board[i][i] = 'X'
        winner = self.play.check_winner()
        self.assertEqual(winner, 'X')
    
    def test_check_winner_anti_diagonal(self):
        """Test anti-diagonal win detection"""
        for i in range(4):
            self.play.board[i][3-i] = 'O'
        winner = self.play.check_winner()
        self.assertEqual(winner, 'O')
    
    def test_check_draw(self):
        """Test draw detection"""
        # Create a board with no winner
        self.play.board = [
            ['X', 'O', 'X', 'O'],
            ['O', 'X', 'O', 'X'],
            ['O', 'X', 'O', 'X'],
            ['X', 'O', 'X', 'O']
        ]
        winner = self.play.check_winner()
        self.assertEqual(winner, 'DRAW')
    
    def test_no_winner_yet(self):
        """Test when game is still in progress"""
        self.play.board[0][0] = 'X'
        self.play.board[1][1] = 'O'
        winner = self.play.check_winner()
        self.assertIsNone(winner)
    
    def test_get_bot_move(self):
        """Test bot move generation"""
        row, col = self.play.get_bot_move()
        self.assertIsNotNone(row)
        self.assertIsNotNone(col)
        self.assertTrue(0 <= row < 4)
        self.assertTrue(0 <= col < 4)
        self.assertEqual(self.play.board[row][col], '-')
    
    def test_get_bot_move_full_board(self):
        """Test bot move when board is full"""
        for i in range(4):
            for j in range(4):
                self.play.board[i][j] = 'X'
        row, col = self.play.get_bot_move()
        self.assertIsNone(row)
        self.assertIsNone(col)
    
    def test_choose_symbol(self):
        """Test symbol selection"""
        # Test X selection
        self.play.player_symbol = 'X'
        self.play.bot_symbol = 'O'
        self.assertEqual(self.play.player_symbol, 'X')
        self.assertEqual(self.play.bot_symbol, 'O')
        
        # Test O selection
        self.play.player_symbol = 'O'
        self.play.bot_symbol = 'X'
        self.assertEqual(self.play.player_symbol, 'O')
        self.assertEqual(self.play.bot_symbol, 'X')
    
    def test_update_stats_win(self):
        """Test stats update on player win"""
        from django.utils import timezone
        self.play.game = Game.objects.create(player=self.player, board_type='4X4')
        self.play.game.start_time = timezone.now()
        
        initial_games = self.player.games_played
        initial_wins = self.player.games_won
        
        self.play.update_stats('X')
        self.player.refresh_from_db()
        
        self.assertEqual(self.player.games_played, initial_games + 1)
        self.assertEqual(self.player.games_won, initial_wins + 1)
    
    def test_update_stats_draw(self):
        """Test stats update on draw"""
        from django.utils import timezone
        self.play.game = Game.objects.create(player=self.player, board_type='4X4')
        self.play.game.start_time = timezone.now()
        
        initial_games = self.player.games_played
        initial_draws = self.player.games_drawn
        
        self.play.update_stats('DRAW')
        self.player.refresh_from_db()
        
        self.assertEqual(self.player.games_played, initial_games + 1)
        self.assertEqual(self.player.games_drawn, initial_draws + 1)
    
    def test_update_stats_loss(self):
        """Test stats update on player loss"""
        from django.utils import timezone
        self.play.game = Game.objects.create(player=self.player, board_type='4X4')
        self.play.game.start_time = timezone.now()
        
        initial_games = self.player.games_played
        initial_wins = self.player.games_won
        
        self.play.update_stats('O')
        self.player.refresh_from_db()
        
        self.assertEqual(self.player.games_played, initial_games + 1)
        self.assertEqual(self.player.games_won, initial_wins)


class PlayerModelTestCase(TestCase):
    def test_create_player(self):
        """Test player creation"""
        player = Player.objects.create_user(username='newplayer', password='pass123')
        self.assertEqual(player.username, 'newplayer')
        self.assertEqual(player.games_played, 0)
        self.assertEqual(player.games_won, 0)
        self.assertEqual(player.games_drawn, 0)
    
    def test_player_str(self):
        """Test player string representation"""
        player = Player.objects.create_user(username='testplayer', password='pass123')
        self.assertEqual(str(player), 'testplayer')


class GameModelTestCase(TestCase):
    def setUp(self):
        self.player = Player.objects.create_user(username='gameplayer', password='pass123')
    
    def test_create_game(self):
        """Test game creation"""
        game = Game.objects.create(player=self.player, board_type='4X4')
        self.assertEqual(game.player, self.player)
        self.assertEqual(game.board_type, '4X4')
        self.assertIsNotNone(game.board)
    
    def test_game_with_winner(self):
        """Test game with winner"""
        game = Game.objects.create(player=self.player, board_type='5X5', winner=self.player)
        self.assertEqual(game.winner, self.player)
