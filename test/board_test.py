import random
import time

import numpy as np

from alphazero.chess_board import ChessBoard

if __name__ == '__main__':

    board = ChessBoard()

    print(board.get_feature_planes())
    print(board.get_available_actions())
    print(board.is_game_over()[0])
