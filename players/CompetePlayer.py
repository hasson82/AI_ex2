"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
import numpy as np
from time import time
from SearchAlgos import AlphaBeta
from state import State, get_utility, get_succ, perform_move, is_goal

# TODO: you can import more modules, if needed


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time,
                                penalty_score)  # keep the inheritance of the parent's (# AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.state = State(True, penalty_score)
        self.penalty_score = penalty_score
        self.mini_max_algo = AlphaBeta(get_utility, get_succ, perform_move,
                                     is_goal)
        self.initialized = False

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
        self.state.set_pos(player_pos, True)
        pos = np.where(board == 2)
        rival_pos = tuple(ax[0] for ax in pos)
        self.state.set_pos(rival_pos, False)
        self.state.set_score(0, True)
        self.state.set_score(0, False)
        if len(self.state.board) < len(self.state.board[0]):
            self.state.num_of_turns_left_for_fruits = 2 * len(self.state.board)
        else:
            self.state.num_of_turns_left_for_fruits = 2 * len(self.state.board[0])

    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        turn_time_limit = time_limit/np.size(self.state.board)
        start_time = time()
        curr_time = time()
        depth = 1
        while curr_time - start_time < 0.35*turn_time_limit:
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
        '''
        self.state.print_state()
        last_positions = np.where(self.state.board == 2)
        last_pos = tuple(ax[0] for ax in last_positions)
        x_dir = pos[0] - last_pos[0]
        y_dir = pos[1] - last_pos[1]
        direction = (x_dir, y_dir)
        self.state = perform_move(self.state, direction, False)
        self.state.switch_turn()
        '''
        board = self.state.board
        new_rival_score = self.state.rival_score + board[pos]
        self.state.check_if_player_ate_fruit(pos)
        board[self.state.get_pos(False)] = -1
        board[pos] = 2
        self.state.num_of_turns_left_for_fruits = self.state.num_of_turns_left_for_fruits - 1
        self.state.set_board(board)
        self.state.set_pos(pos, False)
        self.state.set_score(new_rival_score, False)

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # update
        if not self.initialized:
            self.state.fruit_dict = fruits_on_board_dict
            self.state.fruits_sum = sum(fruits_on_board_dict.values())
            self.initialized = True
        return


    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    ########## helper functions for MiniMax algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm




