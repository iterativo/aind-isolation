"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players

from importlib import reload


class MinimaxPlayerTest(unittest.TestCase):
    """Unit tests for minimax player"""

    def setUp(self):
        reload(game_agent)

    def test_best_score_when_last_layer_is_min_in_shallow_tree(self):
        # Arrange
        self.player1 = game_agent.MinimaxPlayer(
            score_fn=self.fake_score_fn, search_depth=1)
        self.player2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(self.player1, self.player2, width=4, height=4)
        self.game.apply_move((0, 0)) # player 1
        self.game.apply_move((3, 3)) # player 2

        # Act
        best_move = self.player1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(best_move, (1, 2))

    def test_best_score_when_last_layer_is_max_in_shallow_tree(self):
        # Arrange
        self.player1 = game_agent.MinimaxPlayer(
            score_fn=self.fake_score_fn, search_depth=2)
        self.player2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(self.player1, self.player2, width=4, height=4)
        self.game.apply_move((0, 0)) # player 1
        self.game.apply_move((3, 3)) # player 2

        # Act
        best_move = self.player1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(best_move, (2, 1))

    def test_best_score_when_last_layer_is_min_in_deep_tree(self):
        # Arrange
        self.player1 = game_agent.MinimaxPlayer(
            score_fn=self.fake_score_fn, search_depth=3)
        self.player2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(self.player1, self.player2, width=5, height=5)
        self.game.apply_move((0, 0)) # player 1
        self.game.apply_move((4, 4)) # player 2

        # Act
        best_move = self.player1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(best_move, (1, 2))

    def fake_score_fn(self, game, player):
        """Stub score responses here"""

        player1_location = game.get_player_location(player)
        player2_location = game.get_player_location(game.get_opponent(player))
        default_score = 2
        score = {
            ### (player1_location, player2_location): score ###

            # for test_best_score_when_last_layer_is_min_in_shallow_tree
            ((1, 2), (3, 3)): 3,

            # for test_best_score_when_last_layer_is_max_in_shallow_tree
            ((2, 1), (1, 2)): 3,

            # for test_best_score_when_last_layer_is_min_in_deep_tree
            ((2, 0), (3, 2)): 3,
            ((2, 4), (2, 3)): 3
        }
        return score.get((player1_location, player2_location), default_score)


class AlphaBetaPlayerTest(unittest.TestCase):
    """Unit tests for alpha-beta player"""

    def setUp(self):
        reload(game_agent)

    def test_best_score_after_alphabeta_traversal(self):
        # Arrange
        self.player1 = game_agent.AlphaBetaPlayer(
            score_fn=self.fake_score_fn, search_depth=2)
        self.player2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(self.player1, self.player2, width=5, height=5)
        self.game.apply_move((0, 0)) # player 1
        self.game.apply_move((4, 4)) # player 2
        self.score_counter = 4 # to coordinate with fake_score_fn
        self.expected_best_move = None # updated by fake_score_fn

        # Act
        best_move = self.player1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(self.expected_best_move, best_move)

    def test_pruned_brach_is_not_traversed(self):
        # Arrange
        self.player1 = game_agent.AlphaBetaPlayer(
            score_fn=self.fake_score_fn, search_depth=2)
        self.player2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(self.player1, self.player2, width=5, height=5)
        self.game.apply_move((0, 0)) # player 1
        self.game.apply_move((4, 4)) # player 2
        self.score_counter = 4 # to coordinate with fake_score_fn
        self.expected_best_move = None # updated by fake_score_fn

        # Act
        self.player1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(1, self.score_counter, "Pruned branch was traversed")

    def fake_score_fn(self, game, player):
        """
        Stub score responses here.
        Due to the undeterministic nature (since it shuffles its legal_moves)
        we have to keep track of access order to this function and provide
        the proper state values to the test to ensure expected results.
        """

        if self.expected_best_move is None:
            # only the very first time this gets called
            # it stores player's 1 first move in the game
            self.expected_best_move = game.get_player_location(player)

        self.score_counter -= 1
        return self.score_counter


def fake_time_left():
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
