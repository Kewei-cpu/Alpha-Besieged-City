from multiprocessing import Pool

from alphazero import ChessBoard, TerritoryMCTS
from arena import MaxDiffSigmoidTerritory


def match(game_num, c_puct, num_iters=1000):
    results = [0, 0, 0]  # MCTS win-draw-lose

    for game in range(game_num):
        board = ChessBoard()
        terr = MaxDiffSigmoidTerritory(board, error=0.1)
        mcts = TerritoryMCTS(c_puct=c_puct, n_iters=num_iters)

        init_flag = game % 2
        flag = init_flag
        while not board.is_game_over()[0]:
            if flag == 0:
                action = mcts.get_action(board)
            else:
                action = terr.play()
            board.do_action(action)
            flag = 1 - flag

        if board.is_game_over()[1] == init_flag:
            results[0] += 1
        elif board.is_game_over()[1] == 1 - init_flag:
            results[2] += 1
        else:
            results[1] += 1

        print(f"{c_puct=} Matching... {'-'.join(map(str, results))}")
    return results


if __name__ == '__main__':
    pool = Pool()
    results = pool.starmap(match, [(100, 0), (100, 1), (100, 2), (100, 2.5), (100, 3), (100, 3.5), (100, 4)])
    print(results)
    pool.close()
    pool.join()
