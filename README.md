# Ini-ubongIsemin_Vega_TicTacToe
Repo Created For Ini-ubong Isemin's Vega IT Assignment Solution

## TECH STACK
- Python 3.10
- Django 5.0
- SQLite

# Tic Tac Toe Game - Instructions

## How to Play

### Start the Game
```python manage.py playgame```
### Or
```manually run the start_game.py script```

### Game Flow

1. **Login/Signup**: Enter username and password
   - If account exists, you'll be logged in
   - If not, you'll create a new account

2. **Choose Board Size**: Select 4x4 or 5x5 board

3. **Choose Symbol**: Choose X or O

4. **Make Moves**: 
   - Enter position as `row,col` (e.g., `0,0` for top-left)
   - Positions range from `0,0` to `3,3` (4x4) or `4,4` (5x5)

   **CAVEAT:**
   - IN ORDER TO ACCOUNT FOR THE SPECIFIC POSITION OF THE PLAYER'S MOVE, THE PLAYER HAS TO SPECIFY THE COORDINATES WHERE THE SYMBOL WOULD BE POSITIONED. I HAVE ALSO ACCOUNTED FOR THIS BY PRINTING THE COORDINATES OF THE BOARD IN ORDER TO HELP PLAYERS TO EASILY CHOOSE WHERE THEIR SYMBOL GOES

5. **Win Conditions**:
   - Complete row, column, or diagonal with player's symbol
   - Game ends in draw if board is full with no winner

6. **Scoreboard**: After each game, view your stats:
   - Games played
   - Games won/drawn/lost
   - Win rate percentage

7. **Play Again**: Choose to play another round or quit

## Run Tests

```
python manage.py test game_engine
python manage.py test players
```

## Features

- CLI-based gameplay  
- User authentication (login/signup)  
- 4x4 and 5x5 board options  
- Random bot opponent  
- Input validation  
- Win/draw detection  
- Persistent player statistics  
- Session scoreboard with win rate  
- Comprehensive unit tests  
- Modular architecture  

## Architecture

- **game_play.py**: Core game logic
- **models.py**: Database models (Player, Game, Bot, Board)
- **players/**: Player authentication and model
- **management/commands/playgame.py**: CLI entry point
- **tests.py**: Unit tests for all components
