import random
import time

import numpy as np

from alphazero.chess_board import ChessBoard

if __name__ == '__main__':

    board = ChessBoard()
    while True:
        if board.is_game_over()[0]:
            break
        action = random.choice(board.get_available_actions())
        board.do_action(action)
    print(board.get_feature_planes())
