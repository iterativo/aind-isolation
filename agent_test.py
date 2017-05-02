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

    def test_all_nodes_visited_in_shallow_tree(self):
        # Arrange
        self.player_1 = game_agent.MinimaxPlayer(
            score_fn=self.fake_score_increaser_fn, search_depth=1)
        self.player_2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(
            self.player_1, self.player_2, width=9, height=9)
        self.fake_score_increaser = 0
        self.game._board_state = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1,
            1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 65, 68]

        # Act
        best_move = self.player_1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(5, self.fake_score_increaser,
                         "Not every node was visited")

    def test_best_score_when_last_layer_is_min_in_shallow_tree(self):
        # Arrange
        self.player_1 = game_agent.MinimaxPlayer(
            score_fn=self.fake_score_fn, search_depth=1)
        self.player_2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(
            self.player_1, self.player_2, width=4, height=4)
        self.game.apply_move((0, 0))  # player 1
        self.game.apply_move((3, 3))  # player 2

        # Act
        best_move = self.player_1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(best_move, (1, 2))

    def test_best_score_when_last_layer_is_max_in_shallow_tree(self):
        # Arrange
        self.player_1 = game_agent.MinimaxPlayer(
            score_fn=self.fake_score_fn, search_depth=2)
        self.player_2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(
            self.player_1, self.player_2, width=4, height=4)
        self.game.apply_move((0, 0))  # player 1
        self.game.apply_move((3, 3))  # player 2

        # Act
        best_move = self.player_1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(best_move, (2, 1))

    def test_best_score_when_last_layer_is_min_in_deep_tree(self):
        # Arrange
        self.player_1 = game_agent.MinimaxPlayer(
            score_fn=self.fake_score_fn, search_depth=3)
        self.player_2 = sample_players.GreedyPlayer()
        self.game = isolation.Board(
            self.player_1, self.player_2, width=5, height=5)
        self.game.apply_move((0, 0))  # player 1
        self.game.apply_move((4, 4))  # player 2

        # Act
        best_move = self.player_1.get_move(self.game, fake_time_left)

        # Assert
        self.assertEqual(best_move, (1, 2))

    def fake_score_fn(self, game, player):
        """Stub score responses here"""

        player_1_location = game.get_player_location(player)
        player_2_location = game.get_player_location(game.get_opponent(player))
        default_score = 2
        score = {
            # (player_1_location, player_2_location): score

            # for test_best_score_when_last_layer_is_min_in_shallow_tree
            ((1, 2), (3, 3)): 3,

            # for test_best_score_when_last_layer_is_max_in_shallow_tree
            ((2, 1), (1, 2)): 3,

            # for test_best_score_when_last_layer_is_min_in_deep_tree
            ((2, 0), (3, 2)): 3,
            ((2, 4), (2, 3)): 3
        }
        return score.get((player_1_location, player_2_location), default_score)

    def fake_score_increaser_fn(self, game, player):
        """
        Stub score responses with gradual score increase.
        Due to the undeterministic nature (since it shuffles its legal_moves)
        we have to keep track of access order to this function and provide
        the proper state values to the test to ensure expected results.
        """

        self.fake_score_increaser += 1
        return self.fake_score_increaser


# TODO Need to adapt for iterative deepening

# class AlphaBetaPlayerTest(unittest.TestCase):
#     """Unit tests for alpha-beta player"""

#     def setUp(self):
#         reload(game_agent)
#         self.fake_score_increaser = 0  # managed by fake_score_increaser_fn
#         self.fake_score_decreaser = 4  # managed by fake_score_decreaser_fn
#         self.very_first_move = None  # updated by fake scorer functions

#     def test_selection_of_single_legal_move(self):
#         # Arrange
#         self.player_1 = game_agent.AlphaBetaPlayer(
#             score_fn=self.fake_score_decreaser_fn, search_depth=1)
#         self.player_2 = sample_players.GreedyPlayer()
#         self.game = isolation.Board(
#             self.player_1, self.player_2, width=3, height=3)
#         self.game.apply_move((0, 0))  # player 1
#         self.game.apply_move((1, 2))  # player 2

#         # Act
#         best_move = self.player_1.get_move(self.game, fake_time_left)

#         # Assert
#         self.assertEqual((2, 1), best_move)

#     def test_best_score_after_alphabeta_traversal(self):
#         # Arrange
#         self.player_1 = game_agent.AlphaBetaPlayer(
#             score_fn=self.fake_score_decreaser_fn, search_depth=2)
#         self.player_2 = sample_players.GreedyPlayer()
#         self.game = isolation.Board(
#             self.player_1, self.player_2, width=5, height=5)
#         self.game.apply_move((0, 0))  # player 1
#         self.game.apply_move((4, 4))  # player 2

#         # Act
#         best_move = self.player_1.get_move(self.game, fake_time_left)

#         # Assert
#         self.assertEqual(self.very_first_move, best_move)

#     def test_pruned_branch_is_not_traversed(self):
#         # Arrange
#         self.player_1 = game_agent.AlphaBetaPlayer(
#             score_fn=self.fake_score_decreaser_fn, search_depth=2)
#         self.player_2 = sample_players.GreedyPlayer()
#         self.game = isolation.Board(
#             self.player_1, self.player_2, width=5, height=5)
#         self.game.apply_move((0, 0))  # player 1
#         self.game.apply_move((4, 4))  # player 2

#         # Act
#         self.player_1.get_move(self.game, fake_time_left)

#         # Assert
#         self.assertEqual(
#             1, self.fake_score_decreaser, "Pruned branch was traversed")

#     def test_first_move_is_max(self):
#         # Arrange
#         self.player_1 = game_agent.AlphaBetaPlayer(
#             score_fn=self.fake_score_increaser_fn, search_depth=1)
#         self.player_2 = sample_players.GreedyPlayer()
#         self.game = isolation.Board(
#             self.player_1, self.player_2, width=3, height=3)
#         self.game.apply_move((0, 0))  # player 1
#         self.game.apply_move((2, 2))  # player 2

#         # Act
#         best_move = self.player_1.get_move(self.game, fake_time_left)

#         # Assert
#         self.assertNotEqual(self.very_first_move, best_move)

#     def test_second_move_is_min(self):
#         # Arrange
#         self.player_1 = game_agent.AlphaBetaPlayer(
#             score_fn=self.fake_score_fn, search_depth=2)
#         self.player_2 = sample_players.GreedyPlayer()
#         self.game = isolation.Board(
#             self.player_1, self.player_2, width=3, height=3)
#         self.game.apply_move((0, 0))  # player 1
#         self.game.apply_move((2, 2))  # player 2

#         # Act
#         best_move = self.player_1.get_move(self.game, fake_time_left)

#         # Assert
#         self.assertNotEqual((2, 1), best_move)

#     def fake_score_decreaser_fn(self, game, player):
#         """
#         Stub score responses with gradual score decrease.
#         Due to the undeterministic nature (since it shuffles its legal_moves)
#         we have to keep track of access order to this function and provide
#         the proper state values to the test to ensure expected results.
#         """

#         if self.very_first_move is None:
#             self.very_first_move = game.get_player_location(player)

#         self.fake_score_decreaser -= 1
#         return self.fake_score_decreaser

#     def fake_score_increaser_fn(self, game, player):
#         """
#         Stub score responses with gradual score increase.
#         Due to the undeterministic nature (since it shuffles its legal_moves)
#         we have to keep track of access order to this function and provide
#         the proper state values to the test to ensure expected results.
#         """

#         if self.very_first_move is None:
#             self.very_first_move = game.get_player_location(player)

#         self.fake_score_increaser += 1
#         return self.fake_score_increaser

#     def fake_score_fn(self, game, player):
#         """Stub score responses here"""

#         player_1_location = game.get_player_location(player)
#         player_2_location = game.get_player_location(game.get_opponent(player))
#         default_score = 2
#         score = {
#             # (player_1_location, player_2_location): score
#             ((2, 1), (0, 1)): 1,
#             ((2, 1), (1, 0)): 4,
#             ((1, 2), (1, 0)): 2,
#             ((1, 2), (0, 1)): 3
#         }
#         return score.get((player_1_location, player_2_location), default_score)


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


class ScorerFunctionException(Exception):
    pass


if __name__ == '__main__':
    unittest.main()
