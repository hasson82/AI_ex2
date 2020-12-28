from utils import get_directions
from copy import deepcopy
from random import uniform


def get_number_of_open_moves(board, pos):
    open_moves = 0
    for d in get_directions():
        i = pos[0] + d[0]
        j = pos[1] + d[1]
        if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
            open_moves = open_moves + 1
    return open_moves


class State:
    def __init__(self, turn):
        self.turn = turn
        self.board = None
        self.player_pos = None
        self.rival_pos = None
        self.player_score = None
        self.rival_score = None

    def heuristic_func(self):
        if is_goal(self):
            return get_utility(self)
        else:
            return round(uniform(-1, 1), 2)

    def set_board(self, board):
        self.board = board

    def get_pos(self, player):
        if player:
            return self.player_pos
        else:
            return self.rival_pos

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

    def switch_turn(self): # turn is bool: True for player turn, False for rival turn
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
        print("state turn ", self.turn)
        print("\n")


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
    board[pos] = -1
    if player:
        board[new_pos] = 1
    else:
        board[new_pos] = 2
    new_state = State(player)
    new_state.set_board(board)
    new_state.set_pos(state.get_pos(not player), not player)
    new_state.set_score(state.get_score(not player), not player)
    new_state.set_pos(new_pos, player)
    new_state.set_score(score, player)
    return new_state


def is_goal(state):
    directions = get_directions()
    open_moves = 0
    for d in directions:
        if state.turn:
            open_moves = get_number_of_open_moves(state.board, state.player_pos)
        else:
            open_moves = get_number_of_open_moves(state.board, state.rival_pos)
    if open_moves > 0:
        return False
    else:
        return True


def get_utility(state):
    if state.player_score > state.rival_score:
        return 1
    elif state.player_score < state.rival_score:
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
