import math
import random

from alphazero import ChessBoard


class Robot:
    def __init__(self, board: ChessBoard, name=""):
        self.board = board
        self.elo = 1000
        self.name = name

        self.results = []
        self.elos = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def play(self):
        raise NotImplementedError

    def update_elo(self, result, opponent_elo):
        """
        根据对手的elo和比赛结果更新自己的elo
        :param opponent_elo: 对手的elo
        :param result: 比赛结果，1代表胜利，0代表平局，-1代表失败
        :return: None
        """
        k = 32
        self.elo += k * (result - 1 / (1 + 10 ** ((opponent_elo - self.elo) / 400)))

        self.results.append(result)
        self.elos.append(self.elo)


class Random(Robot):
    def __init__(self, board: ChessBoard, name=""):
        super().__init__(board, name)
        if not self.name:
            self.name = "Random Bot"

    def play(self):
        return random.choice(self.board.available_actions)


class Quickest(Robot):
    def __init__(self, board: ChessBoard, name=""):
        super().__init__(board, name)
        if not self.name:
            self.name = "Quickest Bot"

    def play(self):
        for action in self.board.available_actions:
            if action in (50, 48, 49, 51):
                return action


class MaxTerritory(Robot):
    def __init__(self, board: ChessBoard, name=""):
        super().__init__(board, name)
        if not self.name:
            self.name = "Max Territory Bot"

    def terr_function(self, my_distance, enemy_distance):
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

        return 1 if my_distance < enemy_distance else 0 if my_distance > enemy_distance else 0.5

    def get_action_scores(self):
        active_player_pos_index = 0 if self.board.state[12, 0, 0] == 0 else 3
        inactive_player_pos_index = 3 - active_player_pos_index

        all_scores = []

        for action in self.board.available_actions:
            board = self.board.copy()
            board.do_action(action, update_available_actions=False)
            score = 0

            if board.is_game_over()[0]:
                if board.is_game_over()[1] == self.board.state[12, 0, 0]:
                    # 一步杀
                    score = 1
                elif board.is_game_over()[1] == 1 - self.board.state[12, 0, 0]:
                    # 一步死
                    score = -1
                else:
                    # 一步平
                    score = 0

            else:
                active_player_distance = self.board.distance(board.state[active_player_pos_index],
                                                             board.state[inactive_player_pos_index],
                                                             board.state[6],
                                                             board.state[9])
                inactive_player_distance = self.board.distance(board.state[inactive_player_pos_index],
                                                               board.state[active_player_pos_index],
                                                               board.state[6],
                                                               board.state[9])

                for i in range(self.board.board_len):
                    for j in range(self.board.board_len):
                        score += self.terr_function(active_player_distance[i, j],
                                                    inactive_player_distance[i, j]) / self.board.board_len ** 2

            all_scores.append(score)

        return all_scores

    def play(self):
        if random.random() < 0.1:
            # 10%的概率随机走，增加对局多样性
            return random.choice(self.board.available_actions)

        all_scores = self.get_action_scores()
        action = random.choice([a for a, s in zip(self.board.available_actions, all_scores) if s == max(all_scores)])

        return action


class MaxSigmoidTerritory(MaxTerritory):
    def __init__(self, board: ChessBoard, name="", K=2, B=2):
        super().__init__(board, name)
        if not name:
            self.name = "Max Sigmoid Territory Bot"
        self.K = K
        self.B = B

    def terr_function(self, my_distance, enemy_distance):
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

        return 1 / (1 + math.e ** (self.K * (my_distance - enemy_distance) + self.B))


class MaxDictTerritory(MaxTerritory):
    def __init__(self, board: ChessBoard, name="", D=None):
        super().__init__(board, name)
        if not name:
            self.name = "Max Dict Territory Bot"
        if D is None:
            D = dict()
        self.D = D

    def terr_function(self, my_distance, enemy_distance):
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

        if my_distance - enemy_distance in self.D.keys():
            return self.D[my_distance - enemy_distance]
        return 1 if my_distance < enemy_distance else 0 if my_distance > enemy_distance else 0.5


class MaxRelativeSigmoidTerritory(MaxSigmoidTerritory):
    def __init__(self, board: ChessBoard, name="", K=2, B=2):
        super().__init__(board, name, K, B)
        if not name:
            self.name = "Max Diff Sigmoid Territory Bot"

    def get_action_scores(self):
        all_scores = []

        for action in self.board.available_actions:
            board = self.board.copy()
            board.do_action(action, update_available_actions=False)

            if board.is_game_over()[0]:
                if board.is_game_over()[1] == self.board.state[12, 0, 0]:
                    # 一步杀
                    score = 1
                elif board.is_game_over()[1] == 1 - self.board.state[12, 0, 0]:
                    # 一步死
                    score = -1
                else:
                    # 一步平
                    score = 0

            else:
                active_player = 0 if self.board.state[12, 0, 0] == 0 else 3

                active_player_distance = self.board.distance(board.state[active_player],
                                                             board.state[3 - active_player],
                                                             board.state[6],
                                                             board.state[9])
                inactive_player_distance = self.board.distance(board.state[3 - active_player],
                                                               board.state[active_player],
                                                               board.state[6],
                                                               board.state[9])
                active_player_terr = 0
                inactive_player_terr = 0
                all_terr = self.board.board_len ** 2  # 所有格子数

                for i in range(self.board.board_len):
                    for j in range(self.board.board_len):
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
                                active_player_terr += self.terr_function(
                                    active_player_distance[i, j], inactive_player_distance[i, j])

                                inactive_player_terr += self.terr_function(
                                    inactive_player_distance[i, j], active_player_distance[i, j])

                            else:
                                inactive_player_terr += 1

                score = active_player_terr / all_terr
                # score = (active_player_terr - inactive_player_terr) / all_terr

            all_scores.append(score)
        return all_scores
