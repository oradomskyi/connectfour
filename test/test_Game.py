import unittest

from ..Game.Game import Game
from ..Game.Player.PlayerHuman import PlayerHuman
from ..Game.Player.PlayerAlgoRandom import PlayerAlgoRandom


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

        self.width_default = 7
        self.height_default = 6
        self.line_length_default = 4
        self.boring_default = True

        self.board_players_algo = [
            PlayerAlgoRandom(n_moves=self.width_default) for i in range(0, 40)
        ]

        self.settings_default = {
            "players": self.board_players_human,
            "board": {
                "width": self.width_default,
                "height": self.height_default,
                "line_length": self.line_length
            },
            "boring": True
        }

    def test_ctor_correct_args(self):
        """Test the constructor.
        """
        self.board = Game(self.settings_default)
        pass
    
    def tearDown(self):
        """
        """
        pass
