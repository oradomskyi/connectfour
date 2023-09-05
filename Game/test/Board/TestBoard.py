import unittest

from ...Board.Board import Board


class TestBoard(unittest.TestCase):

    def test_initialization(self):
        board = Board(7, 6, 4)
        self.assertEqual(board.get_width(), 7)
        self.assertFalse(board.is_solved())

    def test_next_player_id(self):
        board = Board(7, 6, 4)
        self.assertEqual(board.next_unused_stone(), 0)
        self.assertEqual(board.next_unused_stone(), 1)
        for i in range(2, 41):
            board.next_unused_stone()
        self.assertEqual(board.next_unused_stone(), 41)
        with self.assertRaises(Exception):
            board.next_unused_stone()

    def test_get_symbol(self):
        board = Board(7, 6, 4)
        self.assertEqual(board.get_symbol(0), '▰')

    def test_put_and_apply(self):
        board = Board(7, 6, 4)
        player1_id = board.next_unused_stone()
        player2_id = board.next_unused_stone()
        self.assertTrue(board.apply(0, player1_id, "Player1"))
        self.assertFalse(board.is_solved())
        self.assertTrue(board.apply(1, player2_id, "Player2"))
        self.assertFalse(board.is_solved())

    def test_winning_vertical(self):
        board = Board(7, 6, 4)
        player1_id = board.next_unused_stone()
        self.assertTrue(board.apply(0, player1_id, "Player1"))
        self.assertTrue(board.apply(0, player1_id, "Player1"))
        self.assertTrue(board.apply(0, player1_id, "Player1"))
        self.assertTrue(board.apply(0, player1_id, "Player1"))
        self.assertTrue(board.is_solved())

    def test_winning_horizontal(self):
        board = Board(7, 6, 4)
        player1_id = board.next_unused_stone()
        self.assertTrue(board.apply(0, player1_id, "Player1"))
        self.assertTrue(board.apply(1, player1_id, "Player1"))
        self.assertTrue(board.apply(2, player1_id, "Player1"))
        self.assertTrue(board.apply(3, player1_id, "Player1"))
        self.assertTrue(board.is_solved())


if __name__ == '__main__':
    unittest.main()
