import random
import timeit

import numpy as np

from alphazero import ChessBoard

N = 1000


def main():
    board = ChessBoard()
    for i in range(N):
        while True:
            if board.is_game_over()[0]:
                break
            action = random.choice(board.available_actions)
            board.do_action(action)
        board.clear_board()


if __name__ == '__main__':
    total_time = timeit.timeit(main, number=1)
    print("total time:", total_time)
    print("avg time:", total_time / N)
