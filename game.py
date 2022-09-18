"""This is the main game file."""

from game_exceptions import GameOver, EnemyDown, InvalidInput
from models import Player, Enemy
from settings import GameMode, GameOptions


def play():
    """
    This is a function without parameters that starts the game process.
    """
    while True:
        username = input("Enter your name: ")
        if len(username.strip()):
            break
        print("\nInvalid input :(\n"
              "You must enter your name")
    print("\nThe game has Normal and Hard modes.")
    while True:
        try:
            game_mode = GameMode.game_mode_switch(input("Please enter a mode: "))
            break
        except InvalidInput:
            print("\nInvalid input :(\n"
                  "Please enter 'Normal' or 'Hard'.")
    print("\nEnter 'start' to start the game or 'help' to see other commands.")
    while True:
        try:
            action = GameOptions.action_distributor(input('Enter command: '))
            if action == "start":
                break
        except InvalidInput:
            print("\nInvalid input :(")
    player = Player(username, game_mode)
    level = 1
    enemy_obj = Enemy(level)
    while True:
        try:
            print()
            player.attack(enemy_obj)
            print()
            player.defence(enemy_obj)
        except EnemyDown:
            player.score += GameMode.player_add_score_level_up
            level += 1
            enemy_obj = Enemy(level)
            print(f"\nYou win!!!\nLevel {level}")


if __name__ == '__main__':
    try:
        play()
    except GameOver:
        print("\nGame Over")
    except KeyboardInterrupt:
        pass
    finally:
        print("\nGood bye!")
