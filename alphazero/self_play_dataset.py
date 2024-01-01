# coding:utf-8
from collections import deque, namedtuple

import torch
from torch import Tensor
from torch.utils.data import Dataset

SelfPlayData = namedtuple(
    'SelfPlayData', ['pi_list', 'z_list', 'feature_planes_list'])


class SelfPlayDataSet(Dataset):
    """ 自我博弈数据集类，每个样本为元组 `(feature_planes, pi, z)` """

    def __init__(self, board_len=7):
        super().__init__()
        self.__data_deque = deque(maxlen=10000)
        self.board_len = board_len
        self.flip_dict = {0: 37, 1: 36, 2: 39, 3: 38, 4: 17, 5: 16, 6: 19, 7: 18, 8: 41, 9: 40, 10: 43, 11: 42, 12: 65,
                          13: 64, 14: 67, 15: 66, 16: 5, 17: 4, 18: 7, 19: 6, 20: 21, 21: 20, 22: 23, 23: 22, 24: 45,
                          25: 44, 26: 47, 27: 46, 28: 69, 29: 68, 30: 71, 31: 70, 32: 85, 33: 84, 34: 87, 35: 86, 36: 1,
                          37: 0, 38: 3, 39: 2, 40: 9, 41: 8, 42: 11, 43: 10, 44: 25, 45: 24, 46: 27, 47: 26, 48: 49,
                          49: 48, 50: 51, 51: 50, 52: 73, 53: 72, 54: 75, 55: 74, 56: 89, 57: 88, 58: 91, 59: 90,
                          60: 97, 61: 96, 62: 99, 63: 98, 64: 13, 65: 12, 66: 15, 67: 14, 68: 29, 69: 28, 70: 31,
                          71: 30, 72: 53, 73: 52, 74: 55, 75: 54, 76: 77, 77: 76, 78: 79, 79: 78, 80: 93, 81: 92,
                          82: 95, 83: 94, 84: 33, 85: 32, 86: 35, 87: 34, 88: 57, 89: 56, 90: 59, 91: 58, 92: 81,
                          93: 80, 94: 83, 95: 82, 96: 61, 97: 60, 98: 63, 99: 62}

    def __len__(self):
        return len(self.__data_deque)

    def __getitem__(self, index):
        return self.__data_deque[index]

    def clear(self):
        """ 清空数据集 """
        self.__data_deque.clear()

    def append(self, self_play_data: SelfPlayData):
        """ 向数据集中插入数据 """
        n = self.board_len
        z_list = Tensor(self_play_data.z_list)
        pi_list = self_play_data.pi_list
        feature_planes_list = self_play_data.feature_planes_list
        # 使用翻转和镜像扩充已有数据集
        for z, pi, feature_planes in zip(z_list, pi_list, feature_planes_list):
            self.__data_deque.append((feature_planes, Tensor(pi), z))

            # 沿主对角线翻转
            flip_features = torch.transpose(Tensor(feature_planes.clone().detach()), 1, 2)
            # 翻转后水平和垂直的墙互换
            _ = flip_features.clone().detach()
            flip_features[6:9] = _[9:12]
            flip_features[9:12] = _[6:9]

            flip_pi = torch.zeros_like(Tensor(pi))
            for i in range(len(pi)):
                flip_pi[self.flip_dict[i]] = pi[i]

            self.__data_deque.append((flip_features, flip_pi, z))
