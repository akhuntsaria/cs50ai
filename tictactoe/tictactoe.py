"""
Tic Tac Toe Player
"""

import copy
import math

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
    non_empty = 90
    for row in board:
        for cell in row:
            if cell != EMPTY:
                non_empty += 1
    return X if non_empty % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                res.add((i,j))
    return res


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError
    
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(0,3):
        if board[i][0] != EMPTY and board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] != EMPTY and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
        
    if board[1][1] != EMPTY and ((board[0][0] == board[1][1] and board[1][1] == board[2][2]) or \
        (board[0][2] == board[1][1] and board[1][1] == board[2][0])):
        return board[1][1]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    non_empty = 0
    for row in board:
        for cell in row:
            if cell != EMPTY:
                non_empty += 1
    
    if non_empty == 9:
        return True
    
    if non_empty < 3:
        return False
    
    return winner(board) != None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = winner(board)
    return 1 if res == X else (-1 if res == O else 0)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    plr = player(board)
    res_act = None
    res_utl = None
    for action in actions(board):
        if res_act == None:
            res_act = action
            res_utl = final_utility(result(board, action))
            continue
        
        if plr == X:
            if res_utl == 1:
                break

            utl = final_utility(result(board, action))
            if utl > res_utl:
                res_act = action
                res_utl = utl
        else:
            if res_utl == -1:
                break

            utl = final_utility(result(board, action))
            if utl < res_utl:
                res_act = action
                res_utl = utl

    return res_act

def final_utility(board):
    if terminal(board):
        return utility(board)
    
    action = minimax(board)
    return final_utility(result(board, action))

