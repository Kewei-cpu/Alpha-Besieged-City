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

            self.__data_deque.append((feature_planes, pi.flatten(), z))

            # 沿主对角线翻转
            flip_features = torch.transpose(Tensor(feature_planes), 1, 2)
            flip_pi = torch.transpose(Tensor(pi.reshape(n, n)), 0, 1)
            self.__data_deque.append((flip_features, flip_pi.flatten(), z))
