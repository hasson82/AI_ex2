"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
import numpy as np
from time import time
from SearchAlgos import MiniMax
#TODO: you can import more modules, if needed


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.board = None
        self.pos = None
        self.rival_pos = None
        self.penalty_score = penalty_score
        self.previous_fruit_dict = {}


    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        self.board = board
        pos = np.where(board == 1)
        # convert pos to tuple of ints
        self.pos = tuple(ax[0] for ax in pos)

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        Player player = self
        start_time = time()
        curr_time = time()
        time_taken = curr_time - start_time
        depth = 0
        while time_taken < time_limit:
            direction = MiniMax.search(player , depth, True)
            depth = depth + 1
        return direction


    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        self.board[pos] = -1
        self.rival_pos = pos


    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # update
        new_fruits = set((fruits_on_board_dict.keys()).difference(self.previous_fruit_dict.keys()))
        fruits_to_delete = set((self.previous_fruit_dict.keys()).difference(fruits_on_board_dict.keys()))
        for fruit_pos in new_fruits:
            self.board[fruit_pos] = fruits_on_board_dict[fruit_pos]
        for fruits_pos in fruits_to_delete:
            self.board[fruit_pos] = 0

        self.previous_fruit_dict = fruits_on_board_dict



    ########## helper functions in class ##########
    #TODO: add here helper functions in class, if needed


    ########## helper functions for MiniMax algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm