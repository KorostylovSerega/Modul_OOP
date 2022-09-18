"""This module contains game settings."""

from game_exceptions import InvalidInput

PLAYER_LIVES = 5
HARD_MODE_MULTIPLIER = 3
GAME_COMMANDS = ("start", "scores", "help", "exit")
GAME_MODS = ("NORMAL", "HARD")


class GameMode:
    """
    This class contains methods to game mode.
    """
    player_add_score = 1
    player_add_score_level_up = 5
    enemy_lives_multiplier = 1

    @staticmethod
    def validation_mode(input_mode: str) -> str:
        """
        This is a static method that checks if the game mode
        input is correct.

        Input Arguments:
            input_mode: str
                Game mode entered by the user

        Return:
            str: Game mode
        """
        input_mode = input_mode.strip().upper()
        if input_mode in GAME_MODS:
            return input_mode
        raise InvalidInput

    @staticmethod
    def game_mode_switch(mode: str) -> str:
        """
        This is a static method that enables the game mode.

        Input Arguments:
            mode: str
                Game mode

        Return:
            str: Game mode
        """
        mode = GameMode.validation_mode(mode)
        if mode == "HARD":
            GameMode.player_add_score *= HARD_MODE_MULTIPLIER
            GameMode.player_add_score_level_up *= HARD_MODE_MULTIPLIER
            GameMode.enemy_lives_multiplier *= HARD_MODE_MULTIPLIER
            return mode
        return mode


class GameOptions:
    """
    This class contains all game options
    """

    @staticmethod
    def action_distributor(command: str) -> str:
        """
        This method distributes user commands to other methods.

        Input Arguments:
            command: str
                User input command
        Return:
            str: User input command
        """
        command = command.strip().lower()
        if command in GAME_COMMANDS:
            if command == "start":
                return command
            if command == "scores":
                return GameOptions.game_score(command)
            if command == "help":
                return GameOptions.game_help(command)
            if command == "exit":
                return GameOptions.game_exit()
        raise InvalidInput

    @staticmethod
    def game_help(command: str) -> str:
        """
        This method prints all available game commands
        to the console.

        Input Arguments:
            command: str
                User input command
        Return:
            str: User input command
        """
        print("'start'  --> enter to start the game.\n"
              "'scores' --> enter to show  scores.\n"
              "'exit'   --> enter to exit the game.")
        return command

    @staticmethod
    def game_score(command: str) -> str:
        """
        This method enters the table of results in the console.

        Input Arguments:
            command: str
                User input command
        Return:
            str: User input command
        """
        with open("scores.txt", encoding="utf-8") as file:
            for line in file:
                print(line)
        return command

    @staticmethod
    def game_exit():
        """
        This method has no parameters and throws an
        exception KeyboardInterrupt.
        """
        raise KeyboardInterrupt
