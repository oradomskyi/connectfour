import unittest
from time import sleep

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
            PlayerAlgoRandom(n_moves=self.board_width, max_sleep=0) for i in range(0, 4)
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

    def test_game_initialization(self):
        game = Game(self.settings)
        self.assertEqual(game.board.width, self.board_width)
        self.assertEqual(game.board.height, self.board_height)
        self.assertTrue(all(isinstance(player, PlayerHuman) for player in game.players))

    def test_invalid_settings(self):
        with self.assertRaises(TypeError):
            Game(None)

    def test_game_without_players(self):
        settings_without_players = self.settings.copy()
        settings_without_players.pop("players")
        with self.assertRaises(AttributeError):
            Game(settings_without_players)

    def test_game_sync_mode(self):
        settings = self.settings.copy()
        board_width = 14
        settings["boring"] = True
        settings["board"]["width"] = board_width
        settings["players"] = [
            PlayerAlgoRandom(n_moves=board_width, max_sleep=1) for i in range(0, 4)
        ]

        game = Game(settings)
        game.play()
        while 0 < game.board.empty_cells_left and not game.board.is_solved():
            sleep(1)

        player_moves: list[int] = game.board.get_player_moves()
        two_consecutive_moves = False
        last_id = -1
        for _id in player_moves:
            if last_id == _id:
                two_consecutive_moves = True
                break

            last_id = _id

        print("SYNC player_moves", player_moves)
        self.assertFalse(two_consecutive_moves)

    def test_game_async_mode(self):
        settings = self.settings.copy()
        board_width = 14
        settings["boring"] = False
        settings["board"]["width"] = board_width
        settings["players"] = [
            PlayerAlgoRandom(n_moves=board_width, max_sleep=1) for i in range(0, 4)
        ]

        game = Game(settings)
        game.play()

        while 0 < game.board.empty_cells_left and not game.board.is_solved():
            sleep(1)

        player_moves: list[int] = game.board.get_player_moves()
        two_consecutive_moves = False
        last_id = -1
        for _id in player_moves:
            if last_id == _id:
                two_consecutive_moves = True
                break

            last_id = _id

        print("ASYNC player_moves", player_moves)
        self.assertTrue(two_consecutive_moves)

    def test_large_board_initialization(self):
        large_board_settings = {
            "players": self.board_players_human,
            "board": {
                "width": 50,
                "height": 50,
                "line_length": self.board_line_length
            },
            "boring": self.game_boring
        }
        game = Game(large_board_settings)
        self.assertEqual(game.board.width, 50)
        self.assertEqual(game.board.height, 50)


if __name__ == '__main__':
    runner = unittest.main()