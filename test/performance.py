import cProfile
import pstats
import random
from io import StringIO

import numpy as np

from alphazero import ChessBoard

N = 1000
def main():
    steps = []
    wins = []

    board = ChessBoard()
    for i in range(N):
        while True:
            if board.is_game_over()[0]:
                break
            action = random.choice(board.available_actions)
            board.do_action(action)
        steps.append(board.step_count)
        wins.append(board.is_game_over()[1])
        board.clear_board()

    print("avg step", np.mean(steps))
    print("X wins", wins.count(1))
    print("O wins", wins.count(0))
    print("draws", wins.count(None))


if __name__ == '__main__':
    # 创建一个StringIO来捕获分析结果
    pr = cProfile.Profile()
    pr.enable()

    # 运行你的代码
    main()

    pr.disable()
    s = StringIO()
    sortby = 'time'  # 可以选择不同的排序方式，如 'time', 'calls', 'cumulative' 等
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
