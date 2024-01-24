import json

import numpy as np
from torch import Tensor, tensor
import torch
from tqdm import tqdm

from alphazero import ChessBoard

flip_dict = {0: 37, 1: 36, 2: 39, 3: 38, 4: 17, 5: 16, 6: 19, 7: 18, 8: 41, 9: 40, 10: 43, 11: 42, 12: 65,
                  13: 64, 14: 67, 15: 66, 16: 5, 17: 4, 18: 7, 19: 6, 20: 21, 21: 20, 22: 23, 23: 22, 24: 45,
                  25: 44, 26: 47, 27: 46, 28: 69, 29: 68, 30: 71, 31: 70, 32: 85, 33: 84, 34: 87, 35: 86, 36: 1,
                  37: 0, 38: 3, 39: 2, 40: 9, 41: 8, 42: 11, 43: 10, 44: 25, 45: 24, 46: 27, 47: 26, 48: 49,
                  49: 48, 50: 51, 51: 50, 52: 73, 53: 72, 54: 75, 55: 74, 56: 89, 57: 88, 58: 91, 59: 90,
                  60: 97, 61: 96, 62: 99, 63: 98, 64: 13, 65: 12, 66: 15, 67: 14, 68: 29, 69: 28, 70: 31,
                  71: 30, 72: 53, 73: 52, 74: 55, 75: 54, 76: 77, 77: 76, 78: 79, 79: 78, 80: 93, 81: 92,
                  82: 95, 83: 94, 84: 33, 85: 32, 86: 35, 87: 34, 88: 57, 89: 56, 90: 59, 91: 58, 92: 81,
                  93: 80, 94: 83, 95: 82, 96: 61, 97: 60, 98: 63, 99: 62}

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
    feature_planes_list, pi_list, z_list = get_data(r'./data/match_history_max_vs_max.json')
    data_deque = []

    for z, pi, feature_planes in tqdm(zip(z_list, pi_list, feature_planes_list), ncols=80, desc="Expanding data"):
        data_deque.append((feature_planes, Tensor(pi), z))

        # 沿主对角线翻转
        flip_features = torch.transpose(Tensor(feature_planes.clone().detach()), 1, 2)
        # 翻转后水平和垂直的墙互换
        _ = flip_features.clone().detach()
        flip_features[6:9] = _[9:12]
        flip_features[9:12] = _[6:9]

        flip_pi = torch.zeros_like(Tensor(pi))
        for i in range(len(pi)):
            flip_pi[flip_dict[i]] = pi[i]

        data_deque.append((flip_features, flip_pi, z))

    torch.save(data_deque, './data/data_deque.pth')