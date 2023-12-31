import random
import time

import numpy as np

from alphazero import ChessBoard

if __name__ == '__main__':

    steps = []
    wins = []
    n = 1000
    timer = time.time()
    board = ChessBoard()
    for i in range(n):
        while True:
            if board.is_game_over()[0]:
                break
            action = random.choice(board.available_actions)
            board.do_action(action)
        steps.append(board.step_count)
        wins.append(board.is_game_over()[1])
        board.clear_board()

    print("avg time", (time.time() - timer) / n)
    print("avg step", np.mean(steps))
    print("X wins", wins.count(1))
    print("O wins", wins.count(0))
    print("draws", wins.count(None))
