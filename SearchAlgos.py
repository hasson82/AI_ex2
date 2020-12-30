"""Search Algos: MiniMax, AlphaBeta
"""
from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT
#TODO: you can import more modules, if needed
from state import get_move_between_states

class SearchAlgos:
    def __init__(self, utility, succ, perform_move, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to,
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if self.goal(state) or depth == 0:
            return state.heuristic_func(), None

        if maximizing_player:
            curr_max = float("-inf")
            for c, direction_to_son in self.succ(state, state.get_turn()):
                value, direction = self.search(c, (depth-1), not maximizing_player)
                if value > curr_max:
                    curr_max = value
                    returned_direction = direction_to_son
            return curr_max, returned_direction
        else:
            curr_min = float("inf")
            for c, direction_to_son in self.succ(state, state.get_turn()):
                value, direction = self.search(c, depth-1, not maximizing_player)
                if value < curr_min:
                    curr_min = value
            return curr_min, None


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if self.goal(state) or depth == 0:
            return state.heuristic_func(), None

        if maximizing_player:
            curr_max = float("-inf")
            for c, direction_to_son in self.succ(state, state.get_turn()):
                value, direction = self.search(c, (depth-1), not maximizing_player, alpha, beta)
                if value >= curr_max:
                    curr_max = value
                    returned_direction = direction_to_son
                if curr_max > alpha:
                    alpha = curr_max
                if curr_max >= beta:
                    return float("inf"), None
            return curr_max, returned_direction
        else:
            curr_min = float("inf")
            for c, direction_to_son in self.succ(state, state.get_turn()):
                value, direction = self.search(c, depth-1, not maximizing_player, alpha, beta)
                # print("minimizer: depth", depth, "value", value, "curr min", curr_min, "alpha", alpha, "beta", beta)
                if value <= curr_min:
                    curr_min = value
                if curr_min < beta:
                    beta = curr_min
                if curr_min <= alpha:
                    return float("-inf"), None
            return curr_min, None

