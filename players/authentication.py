from django.contrib.auth import authenticate
from .models import Player

def signup(username: str, password: str):
    player = Player.objects.create_user(
        username=username,
        password=password
    )
    print(player)

    return f"Signup successful! Welcome aboard {player}"

def login(**kwargs):
    player = authenticate(**kwargs)
    print(player)

    if player is not None:
        return "Login successful!"
    else:
        return None
    
