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

    def test_get_move(self):
        self.set_up_minimax(depth=1)
        self.assertEqual(self.player1.get_move(self.game, stubbed_time_left),
            (2, 1))

        # self.set_up_minimax(depth=3)
        # self.assertEqual(self.player1.get_move(self.game, stubbed_time_left),
        #     (2, 1))

    def set_up_minimax(self,
        depth=1,
        player1_start=(0, 0),
        player2_start=(3, 3)):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer(
            score_fn=sample_players.improved_score, search_depth=depth)
        self.player2 = sample_players.RandomPlayer()
        self.game = isolation.Board(self.player1, self.player2, width=4, height=4)
        self.game.apply_move(player1_start)
        self.game.apply_move(player2_start)


def stubbed_time_left():
    return 250  # msecs





def debug(game):
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
