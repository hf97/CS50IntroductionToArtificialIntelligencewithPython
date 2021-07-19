"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # It's the turn of who has less moves
    x = 0
    o = 0
    for row in board:
        for column in row:
            if column == X:
                x += 1
            if column == O:
                o += 1
    if x <= o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # set to prevent duplicates
    moves = set()
    for row_index, row in enumerate(board):
        for column_index, column in enumerate(row):
            if column == EMPTY:
                moves.add((row_index, column_index))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # exception requirement
    if action not in actions(board):
        raise ValueError
    # get whoose turn is
    turn = player(board)
    i,j = action
    # deep copy as said in tip
    new_board = copy.deepcopy(board)
    new_board[i][j] = turn
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontal
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    # check vertical
    for i in range(3):
        column = [board[r][i] for r in range(3)]
        if len(set(column)) == 1:
            return column[0]
    # check diagonal
    diagonal_1 = [board[0][0], board[1][1], board[2][2]]
    if len(set(diagonal_1)) == 1:
        return diagonal_1[0]
    diagonal_2 = [board[0][2], board[1][1], board[2][0]]
    if len(set(diagonal_2)) == 1:
        return diagonal_2[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there is a winner or board e full
    if winner(board) is not None or not actions(board):
        return True
    # game still in progress
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # player_winner to not have to call winner two times
    player_winner = winner(board)
    if player_winner == X:
        return 1
    if player_winner == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # return None if is terminal
    if terminal(board):
        return None
    # get current player
    current_player = player(board)
    # player is X and ai is O
    if current_player == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]
    #

def max_value(board):
    move = ()
    #if is terminal do nothing
    if terminal(board):
        return utility(board), move
    else:
        # value set to -inf an then we want the bigger value in actions
        value = float("-inf")
        for action in actions(board):
            m_value = min_value(result(board, action))[0]
            if m_value > value:
                value = m_value
                move = action
        #return value for using in recursion and move to know what move to perform
        return value, move

def min_value(board):
    move = ()
    #if is terminal do nothing
    if terminal(board):
        return utility(board),move
    else:
        # value set to inf an then we want the smaller value in actions
        value = float("inf")
        for action in actions(board):
            m_value = max_value(result(board, action))[0]
            if m_value < value:
                value = m_value
                move = action
        #return value for using in recursion and move to know what move to perform
        return value,move