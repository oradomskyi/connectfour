import unittest
from unittest.mock import Mock

from ...Player.Player import Player
from ...Board.Board import Board


class TestPlayer(unittest.TestCase):

    def test_random_name_initialization(self):
        player = Player()
        self.assertIsNotNone(player.get_name())
        self.assertTrue(1 <= len(player.get_name()) <= 10)

    def test_given_name_initialization(self):
        name = "TestName"
        player = Player(name=name)
        self.assertEqual(player.get_name(), name)

    def test_set_get_ID(self):
        player = Player()
        test_id = 5
        player.set_ID(test_id)
        self.assertEqual(player.get_ID(), test_id)

    def test_set_get_name(self):
        player = Player()
        name = "NewTestName"
        player.set_name(name)
        self.assertEqual(player.get_name(), name)

    def test_move(self):
        board_mock = Mock(spec=Board)
        input_mock = Mock()
        input_mock.get_int.return_value = 3

        player = Player(_input=input_mock)
        player.move(board_mock)

        board_mock.apply.assert_called_with(
            3,
            player.get_ID(),
            player.get_name()
        )


if __name__ == '__main__':
    runner = unittest.main()