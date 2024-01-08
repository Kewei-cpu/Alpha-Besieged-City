import itertools
import random
import matplotlib.pyplot as plt

from tqdm import tqdm

from alphazero import ChessBoard
from arena import *


class Arena:
    def __init__(self, board: ChessBoard, robots: list[type], param_list: list[dict], N=120):
        """
        :param robots: 机器人的类的列表
        :param N: 每个机器人的对局次数
        """
        self.board = board
        self.robots = [robot(board, **param) for robot, param in zip(robots, param_list)]  # 实例化
        self.N = N

    def generate_matches(self):
        all_matches = []
        for m in itertools.permutations(self.robots, 2):
            all_matches.append(m)
        all_matches *= self.N // (len(self.robots) - 1) // 2
        random.shuffle(all_matches)

        return all_matches

    def match(self):
        for player_blue, player_green in tqdm(self.generate_matches(), ncols=80, desc="Playing"):

            game = Game(self.board, player_blue, player_green)

            blue_score, green_score = game.run()
            blue_elo = player_blue.elo
            green_elo = player_green.elo


            if blue_score > green_score:
                player_blue.update_elo(1, green_elo)
                player_green.update_elo(0, blue_elo)

            elif blue_score < green_score:
                player_blue.update_elo(0, green_elo)
                player_green.update_elo(1, blue_elo)

            else:
                player_blue.update_elo(0.5, green_elo)
                player_green.update_elo(0.5, blue_elo)

        print("==========ELO==========")
        for robot in self.robots:
            print(f"{robot}: {robot.elo:.1f}")
            plt.plot(robot.elos, label=robot.name)
        plt.legend()
        plt.xlabel("Game")
        plt.ylabel("ELO")
        plt.show()



class Game:
    def __init__(self, board: ChessBoard, blue: Robot, green: Robot):
        self.board = board
        self.blue = blue
        self.green = green

    def run(self):
        while True:
            blue_action = self.blue.play()
            self.board.do_action(blue_action)
            if self.board.is_game_over_()[0]:
                blue_score = len(self.board.is_game_over_()[1])
                green_score = len(self.board.is_game_over_()[2])
                self.board.clear_board()
                return blue_score, green_score

            green_action = self.green.play()
            self.board.do_action(green_action)
            if self.board.is_game_over_()[0]:
                blue_score = len(self.board.is_game_over_()[1])
                green_score = len(self.board.is_game_over_()[2])
                self.board.clear_board()
                return blue_score, green_score


if __name__ == '__main__':
    r = [MaxTerritory,] * 3
    p = [
        {"name": "Max 2x+2", "K": 2, "B": 2},
        {"name": "Max 2x+1", "K": 2, "B": 1},
        {"name": "Max 3x+1", "K": 3, "B": 1},
    ]
    # r = [MaxTerritory, MaxTerritory, Random, Random, Quickest, Quickest]
    # p = [{"name": "Max1"}, {"name": "Max2"}, {"name": "Random1"}, {"name": "Random2"}, {"name": "Quickest1"},
    #      {"name": "Quickest2"}]
    # r = [Random, Random, Random, Random, Random, Random]
    # p = [{"name": "Random1"}, {"name": "Random2"}, {"name": "Random3"}, {"name": "Random4"}, {"name": "Random5"}, {"name": "Random6"}]
    arena = Arena(ChessBoard(), robots=r, param_list=p, N=120)
    arena.match()
