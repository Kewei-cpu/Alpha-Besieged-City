# coding: utf-8
import math

import numpy as np

from .chess_board import ChessBoard
from .node import Node


class TerritoryMCTS:
    """ 基于随机走棋策略的蒙特卡洛树搜索 """

    def __init__(self, c_puct: float = 5, n_iters: int = 1000):
        """
        Parameters
        ----------
        c_puct: float
            探索常数

        n_iters: int
            迭代搜索次数
        """
        self.c_puct = c_puct
        self.n_iters = n_iters
        self.root = Node(1, c_puct, parent=None)

    def get_action(self, chess_board: ChessBoard) -> int:
        """ 根据当前局面返回下一步动作

        Parameters
        ----------
        chess_board: ChessBoard
            棋盘
        """
        for i in range(self.n_iters):
            # 拷贝一个棋盘用来模拟
            board = chess_board.copy()

            # 如果没有遇到叶节点，就一直向下搜索并更新棋盘
            node = self.root
            while not node.is_leaf_node():
                action, node = node.select()
                board.do_action(action)

            # 判断游戏是否结束，如果没结束就拓展叶节点
            is_over, winner = board.is_game_over()
            if not is_over:
                node.expand(self.__default_policy(board))

            # 模拟
            value = self.__max_territory_value(board)
            # 反向传播
            node.backup(-value)

        # 根据子节点的访问次数来选择动作
        action = max(self.root.children.items(), key=lambda x: x[1].N)[0]


        # 更新根节点
        self.root = Node(prior_prob=1)
        return action

    def __default_policy(self, chess_board: ChessBoard):
        """ 根据当前局面返回可进行的动作及其概率

        Returns
        -------
        action_probs: List[Tuple[int, float]]
            每个元素都为 `(action, prior_prob)` 元组，根据这个元组创建子节点，
            `action_probs` 的长度为当前棋盘的可用落点的总数
        """
        n = len(chess_board.available_actions)
        probs = np.ones(n) / n
        return zip(chess_board.available_actions, probs)

    def __max_territory_value(self, chess_board: ChessBoard) -> int:
        """
        根据领地大小判断单签局面的价值
        :returns: value
        """

        def terr_function(my_distance, enemy_distance):
            """
            距离 -> 领地计算函数
            :param my_distance: 我方到某一格的距离
            :param enemy_distance: 敌方到某一格的距离
            :return: 领地函数值，0~1，1代表完全为自己领地
            """
            if my_distance == -1:
                return 0

            if enemy_distance == -1:
                return 1

            return 1 / (1 + math.e ** (2 * (my_distance - enemy_distance) + 2))

        if chess_board.is_game_over()[0]:
            if chess_board.is_game_over()[1] == chess_board.state[12, 0, 0]:
                # 一步杀
                score = 1
            elif chess_board.is_game_over()[1] == 1 - chess_board.state[12, 0, 0]:
                # 一步死
                score = -1
            else:
                # 一步平
                score = 0

        else:
            active_player = 0 if chess_board.state[12, 0, 0] == 0 else 3

            active_player_distance = chess_board.distance(chess_board.state[active_player],
                                                          chess_board.state[3 - active_player],
                                                          chess_board.state[6],
                                                          chess_board.state[9])
            inactive_player_distance = chess_board.distance(chess_board.state[3 - active_player],
                                                            chess_board.state[active_player],
                                                            chess_board.state[6],
                                                            chess_board.state[9])
            active_player_terr = 0
            inactive_player_terr = 0
            all_terr = chess_board.board_len ** 2  # 所有格子数

            for i in range(chess_board.board_len):
                for j in range(chess_board.board_len):
                    if inactive_player_distance[i, j] == -1:
                        # 对方无法到达的位置
                        if active_player_distance[i, j] >= 0:
                            # 自己可以到达
                            active_player_terr += 1
                        else:
                            # 自己也无法到达，所有格子数减一
                            all_terr -= 1
                    else:
                        # 对方可以到达的位置
                        if active_player_distance[i, j] >= 0:
                            # 自己可以到达
                            active_player_terr += terr_function(
                                active_player_distance[i, j], inactive_player_distance[i, j])

                            inactive_player_terr += terr_function(
                                inactive_player_distance[i, j], active_player_distance[i, j])

                        else:
                            inactive_player_terr += 1

            score = (active_player_terr - inactive_player_terr) / all_terr

        return score
