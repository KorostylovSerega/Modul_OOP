"""This module contains Player and Enemy classes."""

from random import randrange

from game_exceptions import EnemyDown, GameOver, InvalidInput
from settings import PLAYER_LIVES, GameMode


class Enemy:
    """
    This class contains the methods of the enemy object.
    """

    def __init__(self, level: int):
        """
        This constructor initializes the properties
        of objects of the Enemy class.

        Input Arguments:
            level: int
                Enemy level
        """
        self.level = level
        self.lives = self.level * GameMode.enemy_lives_multiplier

    @staticmethod
    def select_attack():
        """
        This is a static method that selects
        a random character.
        """
        character = randrange(1, 4)
        return character

    def decrease_lives(self):
        """
        This method reduces the amount of life
        an enemy object.
        """
        self.lives -= 1
        if not self.lives:
            raise EnemyDown


class Player:
    """
    This class contains the methods of the player object.
    """
    lives = PLAYER_LIVES
    score = 0
    allowed_attacks = (1, 2, 3)

    def __init__(self, name: str, mode: str):
        """
        This constructor initializes the properties
        of objects of the Player class.

        Input Arguments:
            name: str
                Player name
            mode: str
                Game level
        """
        self.name = name
        self.mode = mode

    @staticmethod
    def fight(attack: int, defense: int) -> int:
        """
        This is a static method that returns
        the result of the duel.

        Input Arguments:
            attack: int
                Character that attacks
            defense: int
                Character who is defending

        Return:
            int: Result of the duel
        """
        result = attack - defense
        if result in (-1, 2):
            return 1
        if result in (-2, 1):
            return -1
        return 0

    def decrease_lives(self):
        """
        This method reduces the life of player.
        """
        self.lives -= 1
        if not self.lives:
            raise GameOver(self)

    def character_validation(self, character: str) -> int:
        """
        This method that controls the correct
        character selection.

        Input Arguments:
            character: str
                Character number

        Return:
            int: Character number
        """
        if character.isdigit():
            if int(character) in self.allowed_attacks:
                return int(character)
        print("\nInvalid input :(\n"
              "You must choose one of the following characters:\n"
              "1 --> WIZARD\n"
              "2 --> WARRIOR\n"
              "3 --> BRIGAND")
        raise InvalidInput

    def attack(self, enemy_obj):
        """
        This method prints a message to the console
        about the result of the attack.
        """
        while True:
            try:
                attack = self.character_validation(input("Enter attack: "))
                break
            except InvalidInput:
                pass
        defence = enemy_obj.select_attack()
        result = self.fight(attack, defence)
        if result == 0:
            print("It's a draw!")
        if result == 1:
            self.score += GameMode.player_add_score
            print("You attacked successfully!")
            enemy_obj.decrease_lives()
        if result == -1:
            print("You missed!")

    def defence(self, enemy_obj):
        """
        This method prints a message about the result
        of protection to the console.
        """
        while True:
            try:
                defence = self.character_validation(input("Enter defence: "))
                break
            except InvalidInput:
                pass
        attack = enemy_obj.select_attack()
        result = self.fight(attack, defence)
        if result == 0:
            print("It's a draw!")
        if result == 1:
            print("You missed!")
            self.decrease_lives()
        if result == -1:
            print("You defenced successfully!")
