"""This is a module with tests for the game."""

from unittest import TestCase
from unittest.mock import patch, mock_open

from game_exceptions import EnemyDown, GameOver, InvalidInput
from models import Enemy, Player
from settings import GameMode, GameOptions


class TestEnemy(TestCase):
    """
    This class contains tests for the Enemy class.
    """

    def test_select_attack(self):
        """
        These are the tests for the select_attack method.
        """
        self.assertIn(Enemy.select_attack(), (1, 2, 3))

    def test_decrease_lives(self):
        """
        These are the tests for the decrease_lives method.
        """
        obj = Enemy(3)
        obj.decrease_lives()
        self.assertEqual(obj.lives, 2)
        self.assertRaises(EnemyDown, Enemy(1).decrease_lives)


class TestPlayer(TestCase):
    """
    This class contains tests for the Player class.
    """

    def setUp(self) -> None:
        self.player = Player('user', 'HARD')

    def test_fight(self):
        """
        These are the tests for the test_fight method.
        """
        self.assertEqual(self.player.fight(3, 1), 1)
        self.assertEqual(self.player.fight(1, 3), -1)
        self.assertEqual(self.player.fight(3, 3), 0)

    @patch('builtins.print')
    def test_decrease_lives(self, mock_print):
        """
        These are the tests for the decrease_lives method.
        """
        self.player.decrease_lives()
        self.assertEqual(self.player.lives, 4)
        self.player.lives = 1
        self.assertRaises(GameOver, self.player.decrease_lives)
        mock_print.assert_called_with("\nPLAYER --> user\n"
                                      "SCORE  --> 0\n"
                                      "MODE   --> HARD")

    @patch('builtins.print')
    def test_character_validation(self, mock_print):
        """
        These are the tests for the character_validation method.
        """
        self.assertEqual(self.player.character_validation('2'), 2)
        self.assertRaises(InvalidInput, self.player.character_validation, '5')
        mock_print.assert_called_with("\nInvalid input :(\n"
                                      "You must choose one of the following characters:\n"
                                      "1 --> WIZARD\n"
                                      "2 --> WARRIOR\n"
                                      "3 --> BRIGAND")
        self.assertRaises(InvalidInput, self.player.character_validation, 'five')

    @patch('builtins.print')
    @patch('models.Enemy.select_attack')
    @patch('builtins.input')
    def test_attack(self, mock_input, mock_sa, mock_print):
        """
        These are the tests for the attack method.
        """
        mock_input.side_effect = ['1', '2', '3']
        mock_sa.side_effect = [3, 2, 1]
        obj = Enemy(1)

        self.player.attack(obj)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(obj.lives, 1)
        mock_print.assert_called_with("You missed!")

        self.player.attack(obj)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(obj.lives, 1)
        mock_print.assert_called_with("It's a draw!")

        self.assertRaises(EnemyDown, self.player.attack, obj)
        self.assertEqual(self.player.score, 1)
        self.assertEqual(obj.lives, 0)
        mock_print.assert_called_with("You attacked successfully!")

    @patch('builtins.print')
    @patch('builtins.input')
    @patch('models.Enemy.select_attack')
    def test_defence(self, mock_sa, mock_input, mock_print):
        """
        These are the tests for the defence method.
        """
        mock_sa.side_effect = [1, 3, 2, 3]
        mock_input.side_effect = ['1', '2', '3', '1']
        obj = Enemy(1)

        self.player.defence(obj)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.lives, 5)
        mock_print.assert_called_with("It's a draw!")

        self.player.defence(obj)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.lives, 5)
        mock_print.assert_called_with("You defenced successfully!")

        self.player.defence(obj)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.lives, 4)
        mock_print.assert_called_with("You missed!")

        self.player.lives = 1
        self.assertRaises(GameOver, self.player.defence, obj)
        self.assertEqual(self.player.score, 0)
        self.assertEqual(self.player.lives, 0)
        mock_print.assert_called_with("\nPLAYER --> user\n"
                                      "SCORE  --> 0\n"
                                      "MODE   --> HARD")


class TestGameOver(TestCase):
    """
    This class contains tests for the GameOver class.
    """

    @patch('builtins.print')
    def test_game_over_initialization(self, mock_print):
        """
        These are the tests for the __init__ method.
        """
        player = Player('name', 'NORMAL')
        obj = GameOver(player)
        self.assertIsInstance(obj, GameOver)
        mock_print.assert_called_with("\nPLAYER --> name\n"
                                      "SCORE  --> 0\n"
                                      "MODE   --> NORMAL")


class TestGameMode(TestCase):
    """
    This class contains tests for the GameMode class.
    """

    def test_validation_mode(self):
        """
        These are the tests for the validation_mode method.
        """
        self.assertEqual(GameMode.validation_mode('normal'), 'NORMAL')
        self.assertEqual(GameMode.validation_mode('Hard'), 'HARD')
        self.assertRaises(InvalidInput, GameMode.validation_mode, 'any_word')

    def test_game_mode_switch(self):
        """
        These are the tests for the game_mode_switch method.
        """
        self.assertEqual(GameMode.game_mode_switch('hard'), 'HARD')
        self.assertEqual(GameMode.player_add_score, 3)
        self.assertEqual(GameMode.player_add_score_level_up, 15)
        self.assertEqual(GameMode.enemy_lives_multiplier, 3)

        GameMode.player_add_score = 1
        GameMode.player_add_score_level_up = 5
        GameMode.enemy_lives_multiplier = 1

        self.assertEqual(GameMode.game_mode_switch('normal'), 'NORMAL')
        self.assertEqual(GameMode.player_add_score, 1)
        self.assertEqual(GameMode.player_add_score_level_up, 5)
        self.assertEqual(GameMode.enemy_lives_multiplier, 1)

        self.assertRaises(InvalidInput, GameMode.game_mode_switch, 'any_word')


class TestGameOptions(TestCase):
    """
    This class contains tests for the GameOptions class.
    """

    @patch('builtins.open', mock_open(read_data='sample_text'))
    @patch('builtins.print')
    def test_action_distributor(self, mock_print):
        """
        These are the tests for the action_distributor method.
        """
        self.assertRaises(InvalidInput, GameOptions.action_distributor, 'any_word')
        self.assertEqual(GameOptions.action_distributor('Start '), 'start')
        self.assertEqual(GameOptions.action_distributor('Scores '), 'scores')
        mock_print.assert_called_with('sample_text')
        self.assertEqual(GameOptions.action_distributor(' Help '), 'help')
        mock_print.assert_called_with("'start'  --> enter to start the game.\n"
                                      "'scores' --> enter to show  scores.\n"
                                      "'exit'   --> enter to exit the game.")
        self.assertRaises(KeyboardInterrupt, GameOptions.action_distributor, 'exit')
