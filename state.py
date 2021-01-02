from utils import get_directions
from copy import deepcopy
import numpy as np


class State:
    def __init__(self, turn, penalty_score):
        self.turn = turn
        self.board = None
        self.player_pos = None
        self.rival_pos = None
        self.player_score = None
        self.rival_score = None
        self.penalty_score = penalty_score
        self.fruits_sum = 0
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.num_of_turns_left_for_fruits = 0
        self.fruit_dict = {}

    def get_portion_of_the_board_closer_to_me(self):
        return self.get_portion_of_the_board_closer_to_me_aux(self.board)

    def get_portion_of_the_board_closer_to_me_aux(self, board):
        pos = np.where(board == 1)
        rival_pos = np.where(board == 2)
        if len(pos[0] > 0):
            player_positions = [(pos[0][i], pos[1][i]) for i in range(len(pos[0]))]
        else:
            player_positions = []
        if len(rival_pos[0] > 0):
            rival_positions = [(rival_pos[0][i], rival_pos[1][i]) for i in range(len(pos[0]))]
        else:
            rival_positions = []
        board = self.board

        if self.turn:
            while len(player_positions) > 0 or len(rival_positions) > 0:
                player_positions, board = get_player_reachable_from_pos(True, player_positions, board, self.directions)
                rival_positions, board = get_player_reachable_from_pos(False, rival_positions, board, self.directions)
        else:
            while len(player_positions) > 0 or len(rival_positions) > 0:
                rival_positions, board = get_player_reachable_from_pos(False, rival_positions, board, self.directions)
                player_positions, board = get_player_reachable_from_pos(True, player_positions, board, self.directions)

        reachable_to_player = len(np.where(board == 1)[0])
        reachable_to_rival = len(np.where(board == 2)[0])
        per_reachable_to_player = reachable_to_player/np.size(board)
        return per_reachable_to_player

    def get_min_open_squares(self):
        num_steps_available = 0
        for d in self.directions:
            i = self.player_pos[0] + d[0]
            j = self.player_pos[1] + d[1]
            # check legal move
            if 0 <= i < len(self.board) and 0 <= j < len(self.board[0]) and (self.board[i][j] not in [-1, 1, 2]):
                num_steps_available += 1

        if num_steps_available == 0:
            return -1
        return 1/(4 - num_steps_available)

    def sum_of_fruits_left(self):
        if len(self.fruit_dict) == 0:
            return 1
        sum_fruits = sum(self.fruit_dict.values())
        return sum_fruits

    def score_advantage(self):
        score_diff = self.player_score - self.rival_score
        # print(self.fruit_sum)
        score_adv_val = score_diff / (self.penalty_score + self.fruits_sum)
        # print(score_adv_val)
        return score_adv_val

    def get_num_of_fruits_closer_to_me(self):
        heuristic_value = 0
        num_of_fruits = 0
        if len(self.fruit_dict) == 0:
            return heuristic_value
        for pos in self.fruit_dict:
            player_distance_to_fruit = (self.player_pos[0] - pos[0]) + (self.player_pos[1] - pos[1])
            rival_distance_to_fruit = (self.rival_pos[0] - pos[0]) + (self.rival_pos[1] - pos[1])
            if player_distance_to_fruit <= rival_distance_to_fruit \
                    and player_distance_to_fruit < self.num_of_turns_left_for_fruits:  # reachable fruit
                num_of_fruits += 1

        return num_of_fruits / len(self.fruit_dict)

    def heuristic_func_aux(self):
        fruits_closer_to_me = self.get_num_of_fruits_closer_to_me()
        score_advantage = self.score_advantage()
        diff_in_percentage_of_reachable = self.get_portion_of_the_board_closer_to_me()
        heuristic_val = 0.1*fruits_closer_to_me + 0.3*score_advantage + 0.5*diff_in_percentage_of_reachable
        if heuristic_val > 1 or heuristic_val < -1:
            print("heuristic val:", heuristic_val)
            print("fruit closer to me heuristic:", 0.0*fruits_closer_to_me)
            print("score advantage heuristic:", 0.0 * score_advantage)
            print("closer to more squares heuristic:", diff_in_percentage_of_reachable)

        return heuristic_val

    def get_num_of_fruits(self):
        counter = 0
        row_len = len(self.board)
        col_len = len(self.board[0])
        for row in range(row_len):
            for col in range(col_len):
                if self.board[row][col] > 2:
                    counter = counter + 1
        return counter

    def get_num_of_open_squares(self):
        counter = 0
        row_len = len(self.board)
        col_len = len(self.board[0])
        for row in range(row_len):
            for col in range(col_len):
                if self.board[row][col] not in [-1, 1, 2]:
                    counter = counter + 1
        return counter

    def heuristic_func(self):
        if is_goal(self):
            utility = get_utility(self)
            return utility
        else:
            val = self.heuristic_func_aux()
            return val

    def set_board(self, board):
        self.board = board

    def get_pos(self, player):
        if player:
            return self.player_pos
        else:
            return self.rival_pos

    def set_state_fruit_dict(self, fruit_dict):
        self.fruit_dict = fruit_dict

    def get_state_fruit_dict(self):
        return self.fruit_dict

    def get_score(self, player):
        if player:
            return self.player_score
        else:
            return self.rival_score

    def set_pos(self, pos, player):
        if player:
            self.player_pos = pos
        else:
            self.rival_pos = pos

    def set_score(self, score, player):
        if player:
            self.player_score = score
        else:
            self.rival_score = score

    def switch_turn(self):  # turn is bool: True for player turn, False for rival turn
        turn = self.turn
        self.turn = not turn

    def get_turn(self):
        return self.turn

    def print_state(self):
        print("\n")
        print("board \n", self.board)
        print("player pos ", self.player_pos)
        print("rival pos ", self.rival_pos)
        print("player score ", self.player_score)
        print("rival score ", self.rival_score)
        print("state fruit dict", self.fruit_dict)
        print("num of turn left for fruits", self.num_of_turns_left_for_fruits)
        print("state turn ", self.turn)
        print("\n")

    def check_if_player_ate_fruit(self, pos):
        if pos in self.fruit_dict:
            del self.fruit_dict[pos]


def perform_move(state, direction, player):
    if player:
        pos = state.player_pos
        score = state.player_score
    else:
        pos = state.rival_pos
        score = state.rival_score
    board = state.board
    new_pos = pos[0] + direction[0], pos[1] + direction[1]
    score += board[new_pos]
    state.check_if_player_ate_fruit(pos)
    fruit_dict = state.fruit_dict
    num_of_turns_left_for_fruits = state.num_of_turns_left_for_fruits - 1
    board[pos] = -1
    if player:
        board[new_pos] = 1
    else:
        board[new_pos] = 2
    board, fruit_dict, num_of_turns_left_for_fruits = update_fruit_knowledge(board, fruit_dict, num_of_turns_left_for_fruits)
    new_state = State(player, state.penalty_score)
    new_state.set_board(board)
    new_state.set_pos(state.get_pos(not player), not player)
    new_state.set_score(state.get_score(not player), not player)
    new_state.set_pos(new_pos, player)
    new_state.set_score(score, player)
    new_state.set_state_fruit_dict(fruit_dict)
    new_state.fruits_sum = state.fruits_sum
    new_state.num_of_turns_left_for_fruits = num_of_turns_left_for_fruits
    return new_state


def is_goal(state):
    if state.turn:
        open_moves = get_number_of_open_moves(state.board, state.player_pos)
    else:
        open_moves = get_number_of_open_moves(state.board, state.rival_pos)
    if open_moves > 0:
        return False
    else:
        return True


def get_utility(state):
    player_score = state.player_score
    rival_score = state.rival_score
    player = state.turn
    if player:
        if get_number_of_open_moves(state.board, state.get_pos(not player)) > 0:
            player_score = player_score - state.penalty_score
    else:
        if get_number_of_open_moves(state.board, state.get_pos(not player)) > 0:
            rival_score = rival_score - state.penalty_score
    if player_score > rival_score:
        return 1
    elif player_score < rival_score:
        return -1
    else:
        return 0


def get_succ(state, player):
    for d in get_directions():
        i = state.get_pos(player)[0] + d[0]
        j = state.get_pos(player)[1] + d[1]
        if (0 <= i < len(state.board)) and (0 <= j < len(state.board[0])) and (state.board[i][j] not in [-1, 1, 2]):
            copied_state = deepcopy(state)
            new_state = perform_move(copied_state, d, state.turn)
            new_state.switch_turn()
            yield new_state, d


def get_move_between_states(initial_state, goal_state):
    initial_pos = initial_state.get_pos(True)
    goal_pos = goal_state.get_pos(True)
    i_dir = goal_pos[0] - initial_pos[0]
    j_dir = goal_pos[1] - initial_pos[1]
    return i_dir, j_dir


def clear_board_from_fruits(board, fruit_dict):
    for pos in fruit_dict:
        board[pos] = 0
    return board


def update_fruit_knowledge(board, fruit_dict, num_of_turns_left_for_fruits):
    if num_of_turns_left_for_fruits == 0:
        board = clear_board_from_fruits(board, fruit_dict)
        fruit_dict = {}
        num_of_turns_left_for_fruits = -1
        return board, fruit_dict, num_of_turns_left_for_fruits
    return board, fruit_dict, num_of_turns_left_for_fruits


def get_number_of_open_moves(board, pos):
    open_moves = 0
    for d in get_directions():
        i = pos[0] + d[0]
        j = pos[1] + d[1]
        if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
            open_moves = open_moves + 1
    return open_moves


def get_player_reachable_from_pos(player, player_positions, board, directions):
    if player:
        player_index = 1
    else:
        player_index = 2
    new_turn_player_positions = []
    for i in range(len(player_positions)):
        pos = player_positions[i]
        for d in directions:
            i = pos[0] + d[0]
            j = pos[1] + d[1]
            # check legal move
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and \
                    (board[i][j] not in [-1, 1, 2]):
                new_turn_player_positions.append((i, j))
                board[(i, j)] = player_index
    player_positions = new_turn_player_positions
    return player_positions, board
