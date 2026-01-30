import random
import copy
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Game, four_by_four, five_by_five
from players.models import Player
from players.authentication import signup, login


class Play:
    def __init__(self):
        self.player = None
        self.game = None
        self.board = None
        self.board_size = 0
        self.player_symbol = 'X'
        self.bot_symbol = 'O'
        
    def authenticate_player(self):
        print("\nWelcome to Tic Tac Toe\n")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        login_result = login(username=username, password=password)
        
        if login_result and "successful" in login_result:
            self.player = Player.objects.get(username=username)
            print(f"\n{login_result}")
            return True
        else:
            print("\nAccount not found. Creating new account...")
            password_two = input("Confirm password: ").strip()
            
            if password != password_two:
                print("Passwords do not match!")
                return False
            
            signup_message = signup(username=username, password=password)
            print(f"\n{signup_message}")
            self.player = Player.objects.get(username=username)
            return True
    
    def choose_symbol(self):
        while True:
            symbol = input("\nChoose your symbol (X or O): ").strip().upper()
            if symbol in ['X', 'O']:
                self.player_symbol = symbol
                self.bot_symbol = 'O' if symbol == 'X' else 'X'
                break
            print("Invalid choice. Please enter X or O.")
    
    def choose_board(self):
        print("\nChoose board size:")
        print("1. 4x4")
        print("2. 5x5")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            self.board = copy.deepcopy(four_by_four)
            self.board_size = 4
            board_type = "4X4"
        elif choice == '2':
            self.board = copy.deepcopy(five_by_five)
            self.board_size = 5
            board_type = "5X5"
        else:
            print("Invalid choice. Defaulting to 4x4")
            self.board = copy.deepcopy(four_by_four)
            self.board_size = 4
            board_type = "4X4"
        
        self.game = Game.objects.create(
            player=self.player,
            board=self.board,
            board_type=board_type
        )
        self.game.start_time = timezone.now()
        
    def print_coordinates(self):
        coordinates = [[(i, j) for j in range(self.board_size)] for i in range(self.board_size)]
        print("\nCoordinates:")
        for row in coordinates:
            print(f"  {row}")
    
    def print_board(self):
        self.print_coordinates()
        print("\nBoard:")
        for i, row in enumerate(self.board):
            print(f"  {' | '.join(row)}")
            if i < len(self.board) - 1:
                print("  " + "-" * (4 * self.board_size - 1))
        print()
    
    def get_player_move(self):
        while True:
            try:
                move = input(f"Enter position (row,col) e.g., 0,0 to {self.board_size-1},{self.board_size-1}: ").strip()
                row, col = map(int, move.split(','))
                
                if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                    print(f"Position must be between 0 and {self.board_size-1}")
                    continue
                
                if self.board[row][col] != '-':
                    print("Position already taken!")
                    continue
                
                return row, col
            except (ValueError, IndexError):
                print("Invalid input! Use format: row,col (e.g., 0,0)")
    
    def get_bot_move(self):
        available_cell = [(i, j) for i in range(self.board_size) 
                     for j in range(self.board_size) if self.board[i][j] == '-']
        
        if available_cell:
            row, col = random.choice(available_cell)
            print(f"Bot plays at ({row},{col})")
            return row, col
        return None, None
    
    def make_move(self, row, col, symbol):
        self.board[row][col] = symbol
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] != '-' and all(cell == row[0] for cell in row):
                return row[0]
        
        # Check columns
        for col in range(self.board_size):
            if self.board[0][col] != '-' and all(self.board[row][col] == self.board[0][col] for row in range(self.board_size)):
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] != '-' and all(self.board[i][i] == self.board[0][0] for i in range(self.board_size)):
            return self.board[0][0]
        
        if self.board[0][self.board_size-1] != '-' and all(self.board[i][self.board_size-1-i] == self.board[0][self.board_size-1] for i in range(self.board_size)):
            return self.board[0][self.board_size-1]
        
        # Check draw
        if all(self.board[i][j] != '-' for i in range(self.board_size) for j in range(self.board_size)):
            return 'DRAW'
        
        return None
    
    def update_stats(self, result):
        self.player.games_played += 1
        
        if result == self.player_symbol:
            self.player.games_won += 1
            self.game.winner = self.player
            print(f"\n Congratulations {self.player.username}! You won!")
        elif result == 'DRAW':
            self.player.games_drawn += 1
            print("\n It's a draw!")
        else:
            print(f"\n Bot wins! Better luck next time.")
        
        self.player.save()
        
        end_time = timezone.now()
        self.game.duration = end_time - self.game.start_time
        self.game.board = self.board
        self.game.save()
    
    def print_scoreboard(self):
        win_rate = (self.player.games_won / self.player.games_played * 100) if self.player.games_played > 0 else 0
        
        print("\n" + "="*40)
        print(f"{'SCOREBOARD':^40}")
        print("="*40)
        print(f"Player: {self.player.username}")
        print(f"Games Played: {self.player.games_played}")
        print(f"Games Won: {self.player.games_won}")
        print(f"Games Drawn: {self.player.games_drawn}")
        print(f"Games Lost: {self.player.games_played - self.player.games_won - self.player.games_drawn}")
        print(f"Win Rate: {win_rate:.1f}%")
        print("="*40 + "\n")
    
    def play_game(self):
        self.choose_symbol()
        self.choose_board()
        self.print_board()
        
        current_player = 'human'
        
        while True:
            if current_player == 'human':
                row, col = self.get_player_move()
                self.make_move(row, col, self.player_symbol)
                current_player = 'bot'
            else:
                row, col = self.get_bot_move()
                if row is not None:
                    self.make_move(row, col, self.bot_symbol)
                current_player = 'human'
            
            self.print_board()
            
            result = self.check_winner()
            if result:
                self.update_stats(result)
                break
    
    def start(self):
        if not self.authenticate_player():
            return
        
        while True:
            self.play_game()
            self.print_scoreboard()
            
            play_again = input("Play again? (y/n): ").strip().lower()
            if play_again != 'y':
                print(f"\nThanks for playing, {self.player.username.capitalize()}! See ya! 👋")
                break
