"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)


class MinimaxPlayerTest(unittest.TestCase):
    """Unit tests for minimax player"""

    def test_best_score_when_last_layer_is_min(self):
        # Arrange
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer(
            score_fn=self.stubbed_score_fn, search_depth=1)
        self.player2 = sample_players.RandomPlayer()
        self.game = isolation.Board(self.player1, self.player2, width=4, height=4)
        self.game.apply_move((0, 0)) # player 1
        self.game.apply_move((3, 3)) # player 2

        # Act
        best_move = self.player1.get_move(self.game, stubbed_time_left)

        # Assert
        self.assertEqual(best_move, (1, 2))

    def test_best_score_when_last_layer_is_max(self):
        # Arrange
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer(
            score_fn=self.stubbed_score_fn, search_depth=2)
        self.player2 = sample_players.RandomPlayer()
        self.game = isolation.Board(self.player1, self.player2, width=4, height=4)
        self.game.apply_move((0, 0)) # player 1
        self.game.apply_move((3, 3)) # player 2

        # Act
        best_move = self.player1.get_move(self.game, stubbed_time_left)

        # Assert
        self.assertEqual(best_move, (2, 1))

    def stubbed_score_fn(self, game, player):
        # last layer is max
        if player == self.player1:
            if game.get_player_location(self.player2) == (1, 2):
                return 4
            if game.get_player_location(self.player2) == (2, 1): # expected selection
                return 1
        # last layer is min
        if player == self.player2:
            if game.get_player_location(self.player1) == (2, 1):
                return 1
            if game.get_player_location(self.player1) == (1, 2): # expected selection
                return 4
        return 2


def stubbed_time_left():
    return 250  # msecs


def debug(game):
    """
    To help with debugging. 
    Prints out game grid and relevant metadata.
    """
    print("\n")
    print("active_player:")
    print(game.active_player)
    print("\n")
    print("get_player_location:")
    print(game.get_player_location(game.active_player))
    print("\n")
    print("legal_moves:")
    print(game.get_legal_moves())
    print("\n")
    print("game board:")
    print(game.to_string())


if __name__ == '__main__':
    unittest.main()
