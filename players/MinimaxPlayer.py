"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
import numpy as np
from time import time
from SearchAlgos import MiniMax
from state import State, get_utility, get_succ, perform_move, is_goal

# TODO: you can import more modules, if needed


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (# AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.state = State(True, penalty_score)
        self.penalty_score = penalty_score
        self.previous_fruit_dict = {}
        self.mini_max_algo = MiniMax(get_utility, get_succ, perform_move,
                                     is_goal)

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.state.set_board(board)
        pos = np.where(board == 1)
        # convert pos to tuple of ints
        player_pos = tuple(ax[0] for ax in pos)
        # print("player position inside game params ", player_pos)
        self.state.set_pos(player_pos, True)
        # print("player position inside state ", self.state.player_pos)
        pos = np.where(board == 2)
        rival_pos = tuple(ax[0] for ax in pos)
        self.state.set_pos(rival_pos, False)
        self.state.set_score(0, True)
        self.state.set_score(0, False)

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        # time based make_move
        '''
        depth = 1
    
        direction, state = self.mini_max_algo.search(self.state, depth, True)
        self.state = state
        depth = depth + 1
        curr_time = time()
        time_taken = curr_time - start_time
        return direction
        '''
        start_time = time()
        epsilon = get_epsilon()
        curr_time = time()
        depth = 1
        while curr_time - start_time < time_limit - next(epsilon):
            value, direction = self.mini_max_algo.search(self.state, depth, True)
            curr_time = time()
            depth = depth + 1
        self.state = perform_move(self.state, direction, True)
        return direction

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        board = self.state.board
        new_rival_score = self.state.rival_score + board[pos]
        self.state.set_score(new_rival_score, False)
        board[self.state.get_pos(False)] = -1
        board[pos] = 2
        self.state.set_board(board)
        self.state.set_pos(pos, False)
    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # update
        board = self.state.board
        fruits_to_delete = set((self.previous_fruit_dict.keys())).difference(set(fruits_on_board_dict.keys()))
        for fruit_pos in fruits_to_delete:
            board[fruit_pos] = 0
        self.state.set_board(board)
        self.previous_fruit_dict = fruits_on_board_dict

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed
def get_epsilon():
    a, b= 0.0025, 0.006
    yield a
    while 1:
        a, b = b, a+b
        yield a
    ########## helper functions for MiniMax algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm




