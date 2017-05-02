"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""

import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Heuristic explanation
    ---------------------
    Combines 2 different strategies:

    1) Comparing the amount of own moves vs the opponent's, in a normalized
       fashion with -1.0 representing the worst possible state, and 1.0 the
       best.
    2) Ability to block the opponent when the next turn belongs to them.

    These strategies are summed up in a weighted manner, with a slightly more
    emphasis on strategy # 1, in order to produce the final score.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # --- relative_mobility
    # own mobility vs opponent's (normalized [-1.0 ... 1.0])
    own_mobility = len(own_moves)
    opp_mobility = len(opp_moves)
    relative_mobility = ((own_mobility - opp_mobility) /
                         max(own_mobility, opp_mobility))

    # --- opponent_block_ability
    # ability to block opponent on next move
    opponent_block_ability = 0
    if game.active_player == player:
        opponent_block_ability = (
            1 if len(set(own_moves) & set(opp_moves)) != 0
            else 0)

    # score is calculated using weights for the normalized params
    return float(55 * relative_mobility +
                 45 * opponent_block_ability)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Heuristic explanation
    ---------------------
    Combines 5 different strategies:

    1) Comparing the amount of own moves vs the opponent's, in a normalized
       fashion with -1.0 representing the worst possible state, and 1.0 the
       best.
    2) A simple count of the number of possible moves for the player.
    3) Evaluating which player is closer to the center of the board, with a
       higher score indicating the player is closer and hence in a better
       position than the opponent.
    4) Ability for the player to take over the center on next move.
    5) Ability to block the opponent when the next turn belongs to them.

    These strategies are summed up in a weighted manner, with a slightly more
    emphasis on strategy # 1, in order to produce the final score.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    player_location = game.get_player_location(player)
    opponent_location = game.get_player_location(game.get_opponent(player))
    board_center = ((game.width - 1) / 2, (game.height - 1) / 2)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # --- relative_mobility
    # own mobility vs opponent's (normalized [-1.0 ... 1.0])
    own_mobility = len(own_moves)
    opp_mobility = len(opp_moves)
    relative_mobility = ((own_mobility - opp_mobility) /
                         max(own_mobility, opp_mobility))

    # --- relative_center_domination
    # distance to the center relative to the opponent's
    # (the shorter the distance as compared to the opponent's, the better)
    cy, cx = board_center
    py, px = player_location
    oy, ox = opponent_location
    player_distance = (((cx - px) + (cy - py))**2 / (cx + cy)**2)
    opponent_distance = (((cx - ox) + (cy - oy))**2 / (cx + cy)**2)
    relative_center_domination = opponent_distance - player_distance

    # --- center_ability
    # ability to take over the center on next move
    center_ability = 0
    if game.active_player == player:
        center_ability = 1 if (cx, cy) in own_moves else 0

    # --- opponent_block_ability
    # ability to block opponent on next move
    opponent_block_ability = 0
    if game.active_player == player:
        opponent_block_ability = (
            1 if len(set(own_moves) & set(opp_moves)) != 0
            else 0)

    # score is calculated using weights for the normalized params
    return float(60 * relative_mobility +
                 15 * own_mobility +
                 10 * relative_center_domination +
                 5 * center_ability +
                 10 * opponent_block_ability)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Heuristic explanation
    ---------------------
    Combines 2 different strategies:

    1) Determining the ability to block the opponent when the next turn belongs
       to them.
    2) A simple count of the number of possible moves for the player.

    These strategies are summed up in a weighted manner, with a slightly more
    emphasis on strategy # 1, in order to produce the final score.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # --- own_mobility
    own_mobility = len(own_moves)

    # --- opponent_block_ability
    # ability to block opponent on next move
    opponent_block_ability = 0
    if game.active_player == player:
        opponent_block_ability = (
            1 if len(set(own_moves) & set(opp_moves)) != 0
            else 0)

    # score is calculated using weights for the params
    return float(10 * opponent_block_ability +
                 2 * own_mobility)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return (-1, -1)

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return self._evaluate_minimax(game, depth)[1]

    def _evaluate_minimax(self, game, depth, maximize=True):
        """Evaluates nodes per minimax logic

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximize : boolean
            True if it's a maximize node. False otherwise.

        Returns
        -------
        tuple
            (score, move)
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()
        if not moves:
            return game.utility(self), (-1, -1)

        if depth == 0:
            return self.score(game, self), (-1, -1)

        best_move = (-1, -1)
        if maximize:
            # maximize
            best_score = float("-inf")
            for m in moves:
                forecast = game.forecast_move(m)
                score, _ = self._evaluate_minimax(forecast, depth - 1, False)
                if score > best_score:
                    best_score, best_move = score, m
        else:
            # minimize
            best_score = float("inf")
            for m in moves:
                forecast = game.forecast_move(m)
                score, _ = self._evaluate_minimax(forecast, depth - 1, True)
                if score < best_score:
                    best_score, best_move = score, m
        return best_score, best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.alphabeta(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        return (-1, -1)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return self._evaluate_alphabeta(game, depth, alpha, beta)[1]

    def _evaluate_alphabeta(self, game, depth, alpha, beta, maximize=True):
        """Evaluates node per alphabeta logic

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        tuple
            (score, move)
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()
        if not moves:
            return game.utility(self), (-1, -1)

        if depth == 0:
            return self.score(game, self), (-1, -1)

        best_move = (-1, -1)
        if maximize:
            # maximize
            best_score = float("-inf")
            for m in moves:
                forecast = game.forecast_move(m)
                score, _ = self._evaluate_alphabeta(
                    forecast, depth - 1, alpha, beta, False)
                if score > best_score:
                    best_score, best_move = score, m
                if best_score >= beta:
                    # prune if applicable
                    break
                alpha = max(alpha, best_score)
        else:
            # minimize
            best_score = float("inf")
            for m in moves:
                forecast = game.forecast_move(m)
                score, _ = self._evaluate_alphabeta(
                    forecast, depth - 1, alpha, beta, True)
                if score < best_score:
                    best_score, best_move = score, m
                if best_score <= alpha:
                    # prune if applicable
                    break
                beta = min(beta, best_score)
        return best_score, best_move


def debug(depth, key, value):
    """
    To help with debugging.
    Indents debug output lines per their context place in the search tree.
    """
    indentation = "___" * depth
    print(indentation, key, ":", value)
