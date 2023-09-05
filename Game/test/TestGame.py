import unittest

from ..Game import Game
from ..Player.PlayerHuman import PlayerHuman
from ..Player.PlayerAlgoRandom import PlayerAlgoRandom


class TestGame(unittest.TestCase):
    """Unit-testing the Game class"""

    def setUp(self):
        """Prepare parts of the settings dict to test instantiation of Board.
        """

        self.board_players_human = [
            PlayerHuman(
                name="Fede",
                phrases=[' ', 'Well-well...', 'Ha!', 'Ough.']
            ),
            PlayerHuman(
                name="Ale",
                phrases=[
                    ' ',
                    'Weeee!',
                    'A-ha-ha!',
                    '*sneezing*',
                    '*scratches the head*',
                    '*crying in Korean*',
                ]
            )
        ]

        self.board_width = 7
        self.board_height = 6
        self.board_line_length = 4
        self.game_boring = True

        self.board_players_algo = [
            PlayerAlgoRandom(n_moves=self.board_width) for i in range(0, 40)
        ]

        self.settings = {
            "players": self.board_players_human,
            "board": {
                "width": self.board_width,
                "height": self.board_height,
                "line_length": self.board_line_length
            },
            "boring": self.game_boring
        }

    def test_ctor_correct_args(self):
        """Test the constructor with correct input args.
        """
        game = Game(self.settings)
        self.assertEqual(game.board.width, self.board_width)
        self.assertEqual(game.board.height, self.board_height)
        self.assertTrue(all(isinstance(player, PlayerHuman) for player in game.players))

    def tearDown(self):
        """
        """
        pass
