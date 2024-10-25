"""
Tic Tac Toe Player
"""

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

    # Check whether board is in play
    if terminal(board):
        return None

    # Iterate over board to count number of X and O
    X_size = O_size = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == X:
                X_size += 1
            elif board[i][j] == O:
                O_size += 1

    # Return player who has next turn
    if X_size == O_size:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Check whether board is in play
    if terminal(board):
        return None

    # Iterate over the board to find empty cells
    EMPTY_set = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                EMPTY_set.add((i, j))

    # Return set of all possible actions (i, j) on board
    return EMPTY_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Ensure action is valid
    if action not in actions(board):
        raise ValueError

    # Make action on the board
    result_board = copy.deepcopy(board)
    result_board[action[0]][action[1]] = player(board)

    # Return resulting board from action
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check for row winner
    for i in range(len(board)):
        if board[i][0] is not EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]

    # Check for column winner
    for i in range(len(board[0])):
        if board[1][i] is not EMPTY and board[0][i] == board[1][i] == board[2][i]:
            return board[1][i]

    # Check for diagonal winner
    if board[2][2] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[2][2]

    # Check for anti-diagonal winner
    if board[2][0] is not EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # No winner at present
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Check for winner
    if winner(board) is not None:
        return True

    # Check for empty cells
    for i in range(len(board)):
        for j in range(len(board[1])):
            if board[i][j] == EMPTY:
                return False

    # Else the game tied
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    # Get winner of board
    champion = winner(board)

    # Find who is the winner
    if champion == X:
        return 1
    elif champion == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Check whether game ended
    if terminal(board):
        return None

    # Get utilities for all moves
    current_player = player(board)
    moves = actions(board)
    utilities = {}
    def play(board):
        """
        Returns the utility of the current board
        """

        # Check whether game ended
        if terminal(board):
            return utility(board)

        # Get utilities for each move
        moves = actions(board)
        if player(board) == current_player:
            return max((play(result(board, move)) for move in moves))
        else:
            return min((play(result(board, move)) for move in moves))
    for move in moves:
        utilities[move] = play(result(board, move))

    # Get optimal action
    if current_player == X:
        return max(utilities, key=utilities.get)
    else:
        return min(utilities, key=utilities.get)
