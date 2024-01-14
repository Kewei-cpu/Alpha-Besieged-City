import itertools
import random

from tqdm import tqdm

from alphazero import ChessBoard
from arena import *


class Arena:
    def __init__(self, robots: list[type], param_list: list[dict], N=120):
        """
        :param robots: 机器人的类的列表
        :param N: 每个机器人的对局次数
        """
        self.board = ChessBoard()
        self.robots = [robot(self.board, **param) for robot, param in zip(robots, param_list)]  # 实例化
        self.all_games = []
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

            blue_score, green_score, game_moves = game.run()

            self.all_games.append(game_moves)

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

        return self.all_games


class Game:
    def __init__(self, board: ChessBoard, blue: Robot, green: Robot):
        self.board = board
        self.blue = blue
        self.green = green
        self.all_moves = []

    def run(self):
        while True:
            blue_action = self.blue.play()
            self.all_moves.append(blue_action)
            self.board.do_action(blue_action)
            if self.board.is_game_over_()[0]:
                blue_score = len(self.board.is_game_over_()[1])
                green_score = len(self.board.is_game_over_()[2])
                self.board.clear_board()
                return blue_score, green_score, self.all_moves

            green_action = self.green.play()
            self.all_moves.append(green_action)
            self.board.do_action(green_action)
            if self.board.is_game_over_()[0]:
                blue_score = len(self.board.is_game_over_()[1])
                green_score = len(self.board.is_game_over_()[2])
                self.board.clear_board()
                return blue_score, green_score, self.all_moves
