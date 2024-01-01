import random

import torch
from torch import Tensor

from alphazero.chess_board import ChessBoard

if __name__ == '__main__':
    board = ChessBoard()

    for i in range(10):
        board = ChessBoard()
        while True:
            if board.is_game_over()[0]:
                break
            action = random.choice(board.get_available_actions())
            board.do_action(action)

    feature_planes = board.get_feature_planes()
    print(feature_planes[6])
    print("-" * 20)

    # # 沿主对角线翻转
    flip_features = torch.transpose(feature_planes.clone().detach(), 1, 2)
    # # 翻转后水平和垂直的墙互换
    _ = flip_features.clone().detach()
    flip_features[6:9] = _[9:12]
    flip_features[9:12] = _[6:9]

    print(feature_planes[6])
    print("-" * 20)
    print(flip_features[9])

