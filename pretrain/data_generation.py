import json

import numpy as np
from torch import Tensor, tensor
import torch
from tqdm import tqdm

from alphazero import ChessBoard




def get_data(data_path, board_len=7):
    """ 从历史记录中获取训练数据

    Parameters
    ----------
    data_path: str
        历史记录

    board_len: int
        棋盘大小

    Returns
    -------
    X: np.ndarray
        输入数据

    Y: np.ndarray
        标签数据
    """

    with open(data_path, 'r', encoding='utf-8') as f:
        history = json.load(f)

    X = []
    Y1 = []
    Y2 = []
    board = ChessBoard(board_len)

    for game in tqdm(history, ncols=80, desc="Generating data"):
        board.clear_board()
        players = []

        feature_list = []
        pi_list = []

        for action in game:
            players.append(board.state[12, 0, 0])
            feature_list.append(board.get_feature_planes())
            pi_list.append(action)

            board.do_action(action)

        _, winner = board.is_game_over()
        gamma = 0.8
        if winner is not None:
            z_list = []
            # 最后一步价值为1，每向前一步价值乘以gamma
            for i in range(len(players)):
                if players[i] == winner:
                    z_list.append(gamma ** (players[i:].count(winner) - 1))
                else:
                    z_list.append(-gamma ** (players[i:].count(1 - winner) - 1))
        else:
            z_list = [0 for _ in range(len(players))]

        for i in range(len(feature_list)):
            X.append(feature_list[i])
            one_hot_pi = np.zeros((100, ))
            one_hot_pi[pi_list[i]] = 1
            Y1.append(one_hot_pi)
            Y2.append(z_list[i])


    return torch.from_numpy(np.array(X)), torch.from_numpy(np.array(Y1)),torch.from_numpy(np.array(Y2))


if __name__ == '__main__':
    x, y1, y2 = get_data(r'./data/match_history_max_vs_max.json')

    print(x.shape)
    print(y1.shape)
    print(y2.shape)

    print(x[0])
    print(y1[0])
    print(y2[0])

    print(x[1])
    print(y1[1])
    print(y2[1])

    print(x[2])
    print(y1[2])
    print(y2[2])
