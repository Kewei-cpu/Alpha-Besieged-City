import random
import timeit
from multiprocessing import Pool

from alphazero import ChessBoard

N = 100000


def main(n):
    board = ChessBoard()
    for i in range(n):
        while True:
            if board.is_game_over()[0]:
                break
            action = random.choice(board.available_actions)
            board.do_action(action)
        board.clear_board()


def multiprocess():
    process = 16
    with Pool(process) as pool:
        pool.map(main, [N // process] * process)


if __name__ == '__main__':
    total_time = timeit.timeit(multiprocess, number=1)
    print("total time:", total_time)
    print("avg time:", total_time / N)
    print("Moves/s", N * 22 / total_time)
