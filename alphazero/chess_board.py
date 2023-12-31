# coding: utf-8
from copy import deepcopy
from typing import Tuple, List

import numpy as np
import torch


class ChessBoard:
    """
    棋盘类，用于存储棋盘状态和落子，判断游戏是否结束等
    """

    action_to_pos = {
        0: (-3, 0),
        1: (-2, -1), 2: (-2, 0), 3: (-2, 1),
        4: (-1, -2), 5: (-1, -1), 6: (-1, 0), 7: (-1, 1), 8: (-1, 2),
        9: (0, -3), 10: (0, -2), 11: (0, -1), 12: (0, 0), 13: (0, 1), 14: (0, 2), 15: (0, 3),
        16: (1, -2), 17: (1, -1), 18: (1, 0), 19: (1, 1), 20: (1, 2),
        21: (2, -1), 22: (2, 0), 23: (2, 1),
        24: (3, 0)
    }

    def __init__(self, board_len=7, n_feature_planes=13):
        """
        :param board_len: 棋盘边长
        :param n_feature_planes: 特征平面数
        """

        self.board_len = board_len
        self.n_feature_planes = n_feature_planes

        self.state = np.zeros((self.n_feature_planes, self.board_len, self.board_len), dtype=int)
        # index 0  X 位置
        #       1  X 上一个位置
        #       2  X 上上个位置
        #       3  O 位置
        #       4  O 上一个位置
        #       5  O 上上个位置
        #       6  横向墙 位置
        #       7  横向墙 上一个位置
        #       8  横向墙 上上个位置
        #       9  纵向墙 位置
        #       10 纵向墙 上一个位置
        #       11 纵向墙 上上个位置
        #       12 该谁走了 0 for X ; 1 for O

        self.state[0, 0, 0] = 1  # X 初始在左上角
        self.state[3, self.board_len - 1, self.board_len - 1] = 1  # O 初始在右下角

        self.step_count = 0

        self.available_actions = self.get_available_actions()

    def copy(self) -> 'ChessBoard':
        """ 复制棋盘 """
        return deepcopy(self)

    def clear_board(self):
        """ 清空棋盘 """
        self.state = np.zeros((self.n_feature_planes, self.board_len, self.board_len), dtype=int)
        self.state[0, 0, 0] = 1
        self.state[3, self.board_len - 1, self.board_len - 1] = 1

        self.available_actions = self.get_available_actions()

    def do_action(self, action: int):
        """
        执行动作
        :param action: 动作，范围为 0 ~ 99
        :return:
        """
        # 判断合法性
        if action not in self.available_actions:
            raise ValueError(f'Illegal action {action}')

        # 更新过去历史
        # 仅在轮到某玩家走时更新位置历史
        if self.state[12, 0, 0] == 0:
            for i in (2, 1):
                self.state[i] = self.state[i - 1]
        else:
            for i in (5, 4):
                self.state[i] = self.state[i - 1]

        # 更新墙历史
        for i in (8, 7, 11, 10):
            self.state[i] = self.state[i - 1]

        # MOVE

        move = action // 4
        wall = action % 4

        active_player = 0 if self.state[12, 0, 0] == 0 else 3

        # 更新当前位置
        self.state[active_player] = self.coordinates_to_array(
            [(self.action_to_pos[move][0] + self.array_to_coordinates(self.state[active_player])[0][0],
              self.action_to_pos[move][1] + self.array_to_coordinates(self.state[active_player])[0][1])]
        )

        # 放墙
        if wall == 0:
            self.state[6, self.array_to_coordinates(self.state[active_player])[0][0] - 1,
            self.array_to_coordinates(self.state[active_player])[0][1]] = 1
        elif wall == 1:
            self.state[9, self.array_to_coordinates(self.state[active_player])[0][0],
            self.array_to_coordinates(self.state[active_player])[0][1] - 1] = 1
        elif wall == 2:
            self.state[6, self.array_to_coordinates(self.state[active_player])[0][0],
            self.array_to_coordinates(self.state[active_player])[0][1]] = 1
        elif wall == 3:
            self.state[9, self.array_to_coordinates(self.state[active_player])[0][0],
            self.array_to_coordinates(self.state[active_player])[0][1]] = 1

        # 更新谁该走、合法位置
        self.state[12] = np.ones((self.board_len, self.board_len)) - self.state[12]
        self.available_actions = self.get_available_actions()

        self.step_count += 1

    def is_game_over(self) -> Tuple[bool, int]:
        """
        判断游戏是否结束
        :return: （是否结束， 胜利者） 胜利者为 1 代表 X 胜利， -1 代表 O 胜利， 0 代表平局
        """

        if self.array_to_coordinates(self.state[3])[0] not in \
                self.reachable_positions(self.state[0], self.state[3],
                                         self.state[6], self.state[9],
                                         ignore_other_player=True, step=self.board_len * 2):
            x_territory = self.reachable_positions(self.state[0], self.state[3],
                                                   self.state[6], self.state[9],
                                                   ignore_other_player=True, step=self.board_len * 2)
            o_territory = self.reachable_positions(self.state[3], self.state[0],
                                                   self.state[6], self.state[9],
                                                   ignore_other_player=True, step=self.board_len * 2)
            return True, np.sign(len(x_territory) - len(o_territory))

        return False, 0

    def get_feature_planes(self) -> torch.Tensor:
        """
        获取特征平面
        :return: torch.Tensor of shape (n_feature_planes, board_len, board_len)
        """

        return torch.tensor(self.state)

    def get_available_actions(self) -> List[int]:
        """
        获取当前可用动作
        :return: 动作列表
        """
        active_player_pos = self.state[0] if self.state[12, 0, 0] == 0 else self.state[3]
        passive_player_pos = self.state[3] if self.state[12, 0, 0] == 0 else self.state[0]
        horizontal_wall = self.state[6]
        vertical_wall = self.state[9]

        available_move = []

        for move in range(25):  # 移动位置， 详见self.action_to_pos
            next_pos = (self.action_to_pos[move][0] + self.array_to_coordinates(active_player_pos)[0][0],
                        self.action_to_pos[move][1] + self.array_to_coordinates(active_player_pos)[0][1])
            for wall in range(4):  # 放墙位置， 0-上；1-左；2-下；3-右
                if (next_pos in self.reachable_positions(active_player_pos, passive_player_pos,
                                                         horizontal_wall, vertical_wall)
                        and self.placeable(next_pos, wall, horizontal_wall, vertical_wall)):
                    available_move.append(move * 4 + wall)

        return available_move

    def reachable_positions(self, pos, other_player_pos, horizontal_wall, vertical_wall, step=3,
                            ignore_other_player=False) -> List[Tuple[int, int]]:
        """
        可到达的位置，采用BFS遍历
        :param pos: 起始位置， one-hot编码
        :param other_player_pos: 对方位置， one-hot编码
        :param horizontal_wall: 横向墙， one-hot编码
        :param vertical_wall: 纵向墙， one-hot编码
        :param step: 最大步数（设置为棋盘边长的两倍即可遍历全部位置）
        :param ignore_other_player: 是否忽略对方，True代表可以经过对方位置
        :return: 可到达的位置列表
        """

        pos = self.array_to_coordinates(pos)[0]
        queue = [pos]
        visited = [pos]
        for i in range(step):
            if len(queue) == 0:
                break
            for j in range(len(queue)):
                current = queue.pop(0)
                if current[0] - 1 >= 0 and horizontal_wall[current[0] - 1][current[1]] == 0 and (
                        current[0] - 1, current[1]) not in visited and (
                        not other_player_pos[current[0] - 1, current[1]] or ignore_other_player):
                    queue.append((current[0] - 1, current[1]))
                    visited.append((current[0] - 1, current[1]))
                if current[1] - 1 >= 0 and vertical_wall[current[0]][current[1] - 1] == 0 and (
                        current[0], current[1] - 1) not in visited and (
                        not other_player_pos[current[0], current[1] - 1] or ignore_other_player):
                    queue.append((current[0], current[1] - 1))
                    visited.append((current[0], current[1] - 1))
                if current[0] + 1 < self.board_len and horizontal_wall[current[0]][current[1]] == 0 and (
                        current[0] + 1, current[1]) not in visited and (
                        not other_player_pos[current[0] + 1, current[1]] or ignore_other_player):
                    queue.append((current[0] + 1, current[1]))
                    visited.append((current[0] + 1, current[1]))
                if current[1] + 1 < self.board_len and vertical_wall[current[0]][current[1]] == 0 and (
                        current[0], current[1] + 1) not in visited and (
                        not other_player_pos[current[0], current[1] + 1] or ignore_other_player):
                    queue.append((current[0], current[1] + 1))
                    visited.append((current[0], current[1] + 1))

        return visited

    def placeable(self, pos, place, horizontal_wall, vertical_wall) -> bool:
        """
        当前位置，当前放置方式是否可行
        :param pos: 当前位置，以坐标形式，不是one-hot编码！！！
        :param place: 当前放置方式，0-上；1-左；2-下；3-右
        :param horizontal_wall: 横向墙， one-hot编码
        :param vertical_wall: 纵向墙， one-hot编码
        :return: 是否可行
        """
        # pos = self.array_to_coordinates(pos)[0]
        if place == 0:
            if pos[0] - 1 < 0 or horizontal_wall[pos[0] - 1][pos[1]] == 1:
                return False
        elif place == 1:
            if pos[1] - 1 < 0 or vertical_wall[pos[0]][pos[1] - 1] == 1:
                return False
        elif place == 2:
            if pos[0] + 1 >= self.board_len or horizontal_wall[pos[0]][pos[1]] == 1:
                return False
        elif place == 3:
            if pos[1] + 1 >= self.board_len or vertical_wall[pos[0]][pos[1]] == 1:
                return False
        return True

    @staticmethod
    def array_to_coordinates(array: np.ndarray) -> List[Tuple[int, int]]:
        """
        找出2D数组中所有为1的位置
        :param array: 2维数组
        :return: 1的位置列表，注意即使只有一个1，也是列表
        """
        coordinates = []
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                if array[i][j] == 1:
                    coordinates.append((i, j))
        return coordinates

    @staticmethod
    def coordinates_to_array(coordinates: list, shape: tuple = (7, 7)) -> np.ndarray:
        """
        根据坐标列表生成2D数组
        :param coordinates: 坐标列表
        :param shape: 2D数组形状
        :return: 2D数组，只有坐标列表中的位置为1，其余为0
        """
        array = np.zeros(shape=shape, dtype=int)
        for coordinate in coordinates:
            array[coordinate[0]][coordinate[1]] = 1
        return array
