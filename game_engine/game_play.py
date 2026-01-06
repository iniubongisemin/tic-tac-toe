import random
import copy
from django.utils import timezone
from .models import Game, four_by_four, five_by_five
from players.models import Player
from players.authentication import signup, login


class Play:
    def __init__(self):
        self.player = None
        self.game = None
        self.board = None
        self.board_size = 0
        self.player_symbol = "X"
        self.bot_symbol = "O"

    def authenticate_player(self):
        print("\nWelcome to Tic Tac Toe \n")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        login_result = login(username=username, password=password)

        if login_result and "successful" in login_result:
            self.player = Player.objects.get(username=username)
            print(f"\n{login_result}")
            return True
        else:
            print("\nAccount not found. Creating new account....")
            password_two = input("Confirm password: ").strip()

            if password_two != password:
                print("Passwords do not match! ")
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
            print(f"Invalid choice. Please enter X or O.")

    def choose_board(self):
        print("\nChoose board size:")
        print("1. 4x4")
        print("1. 5x5")

        choice = input("Enter choice (1 or 2): ").strip()

        if choice == "1":
            self.board = copy.deepcopy(four_by_four)
            self.board_size = 4
            board_type = "4X4"
        elif choice == "2":
            self.board = copy.deepcopy(five_by_five)
            self.board_size = 5
            board_type = "5X5"
        else:
            print("Invalid choice. Defaulting to 4X4")
            self.board_size = 4
            board_type = "4x4"

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
        print("\nBoard")
        for i, row in enumerate(self.board):
            print(f" {' | '.join(row)}")
            if i < len(self.board) - 1:
                print(" " + "-" * (4 * self.board_size - 1))
    
    def get_player_move(self):
        pass
            
            