import json
import os
import sys
import time

import pygame
from pygame.locals import *

from alphazero import ChessBoard
from arena import *


class Game:
    WHITE = (255, 255, 255)
    BLUE = (130, 175, 214)
    GREEN = (80, 181, 142)
    GREY = (128, 128, 128)
    BLACK = (0, 0, 0)

    def __init__(self, board_len, grid_size, border_size, padding_size, robots):
        """
        :param padding_size: 每个棋盘格的间距
        :param grid_num: 棋盘格数量
        :param grid_size: 棋盘格大小
        :param border_size: 棋盘边缘空白大小
        :param robots: 机器人，元组，空代表没有机器人，（0，）代表蓝方为机器人，（0,1） 代表双方都为机器人
        """
        self.border_size = border_size
        self.grid_size = grid_size
        self.board_len = board_len
        self.window_size = board_len * grid_size + border_size * 2
        self.padding_size = padding_size
        self.running = True
        self.board = ChessBoard(board_len)
        self.robots = [i[0](self.board, **i[1]) if i else None for i in robots]
        self.active_player_pos_index = 0
        self.active_player_color = self.BLUE
        self.blue_final_territory = []
        self.green_final_territory = []
        self.history = []
        self.all_games = []

    def display(self, scr):
        """
        显示游戏
        :param scr: 屏幕
        :return:
        """
        self.draw_background(scr)
        self.draw_board(scr)
        if self.running:
            self.draw_available_positions(scr)
            self.draw_players(scr)
            self.draw_active_player(scr)
            self.draw_action_preview(scr)
        else:
            self.draw_final_territory(scr)
            self.draw_dead_player(scr)
        self.draw_wall(scr)

    def draw_background(self, scr):
        """
        绘制渐变背景
        :param scr: 屏幕
        :return:
        """
        for i in range(self.window_size):
            pygame.draw.line(
                scr,
                color=(int(173 - 29 * i / self.window_size),
                       int(124 + 13 * i / self.window_size),
                       int(170 + 1 * i / self.window_size),),
                start_pos=(0, i),
                end_pos=(i, 0),
                width=1,
            )

        for i in range(self.window_size):
            pygame.draw.line(
                scr,
                color=(int(144 - 29 * i / self.window_size),
                       int(137 + 13 * i / self.window_size),
                       int(171 + 1 * i / self.window_size),),
                start_pos=(self.window_size - 1, i),
                end_pos=(i, self.window_size - 1),
                width=1,
            )

    def draw_board(self, scr):
        """
        绘制棋盘（白色正方形）
        :param scr: 屏幕
        :return:
        """
        for i in range(self.board_len):
            for j in range(self.board_len):
                pygame.draw.rect(
                    surface=scr,
                    color=self.WHITE,
                    rect=(self.border_size + j * self.grid_size + self.padding_size // 2,
                          self.border_size + i * self.grid_size + self.padding_size // 2,
                          self.grid_size - self.padding_size,
                          self.grid_size - self.padding_size),
                    border_radius=0
                )

    def draw_players(self, scr):
        """
        绘制玩家
        :param scr:屏幕
        :return:
        """

        pygame.draw.circle(
            surface=scr,
            color=self.BLUE,
            center=(self.border_size + (self.board.player_pos[0][1] + 0.5) * self.grid_size,
                    self.border_size + (self.board.player_pos[0][0] + 0.5) * self.grid_size),
            radius=self.grid_size * 0.3,
        )
        pygame.draw.circle(
            surface=scr,
            color=self.GREEN,
            center=(self.border_size + (self.board.player_pos[1][1] + 0.5) * self.grid_size,
                    self.border_size + (self.board.player_pos[1][0] + 0.5) * self.grid_size),
            radius=self.grid_size * 0.3,
        )

    def draw_active_player(self, scr):
        """
        绘制当前玩家（深色外框）
        :param scr: 屏幕
        :return:
        """

        color = self.BLUE if self.board.state[12, 0, 0] == 0 else self.GREEN
        pos = self.board.player_pos[int(self.board.state[12, 0, 0])]

        pygame.draw.circle(
            surface=scr,
            color=[int(color * 0.7) for color in color],
            center=(self.border_size + (pos[1] + 0.5) * self.grid_size,
                    self.border_size + (pos[0] + 0.5) * self.grid_size),
            width=5,
            radius=self.grid_size * 0.3,
        )

    def draw_dead_player(self, scr):
        """
        显示死亡玩家
        :param scr: 屏幕
        :return:
        """

        pygame.draw.circle(
            surface=scr,
            color=[int(color * 0.7) for color in self.BLUE],
            center=(self.border_size + (self.board.player_pos[0][1] + 0.5) * self.grid_size,
                    self.border_size + (self.board.player_pos[0][0] + 0.5) * self.grid_size),
            radius=self.grid_size * 0.3,
            width=self.padding_size // 4,
        )
        pygame.draw.circle(
            surface=scr,
            color=[int(color * 0.7) for color in self.GREEN],
            center=(self.border_size + (self.board.player_pos[1][1] + 0.5) * self.grid_size,
                    self.border_size + (self.board.player_pos[1][0] + 0.5) * self.grid_size),
            radius=self.grid_size * 0.3,
            width=self.padding_size // 4,
        )

    def draw_action_preview(self, scr):
        """
        显示动作预览（跟随鼠标）
        :param scr: 屏幕
        :return:
        """
        if self.mouse_pos_to_action(pygame.mouse.get_pos()) not in self.board.available_actions:
            return

        move = self.board.action_to_pos[self.mouse_pos_to_action(pygame.mouse.get_pos()) // 4]
        wall = self.mouse_pos_to_action(pygame.mouse.get_pos()) % 4

        destination = (self.board.player_pos[int(self.board.state[12, 0, 0])][0] + move[0],
                       self.board.player_pos[int(self.board.state[12, 0, 0])][1] + move[1])

        if wall == 0:
            self.draw_horizontal_wall(scr, self.active_player_color, destination[0] - 1, destination[1])
        elif wall == 1:
            self.draw_vertical_wall(scr, self.active_player_color, destination[0], destination[1] - 1)
        elif wall == 2:
            self.draw_horizontal_wall(scr, self.active_player_color, destination[0], destination[1])
        elif wall == 3:
            self.draw_vertical_wall(scr, self.active_player_color, destination[0], destination[1])

        pygame.draw.circle(
            surface=scr,
            color=[int(255 - (255 - i) * 0.5) for i in self.active_player_color],
            center=(self.border_size + (destination[1] + 0.5) * self.grid_size,
                    self.border_size + (destination[0] + 0.5) * self.grid_size),
            radius=self.grid_size * 0.3,
        )

    def draw_available_positions(self, scr):
        """
        显示可移动位置
        :param scr: 屏幕
        :return:
        """
        available_positions = []
        for action in self.board.available_actions:
            pos = (self.board.action_to_pos[action // 4][0] +
                   self.board.player_pos[int(self.board.state[12, 0, 0])][0],
                   self.board.action_to_pos[action // 4][1] +
                   self.board.player_pos[int(self.board.state[12, 0, 0])][1]
                   )
            if pos not in available_positions:
                available_positions.append(pos)

        light_color = [int(255 - (255 - i) * 0.9) for i in self.active_player_color]

        for pos in available_positions:
            ## gradient color on 4 edges by drawing smaller and smaller rects
            for i in range((self.grid_size - self.padding_size) // 6):
                pygame.draw.rect(scr, (
                    int(light_color[0] * (1 - i / ((self.grid_size - self.padding_size) // 6))) +
                    255 * i / ((self.grid_size - self.padding_size) // 6),
                    int(light_color[1] * (1 - i / ((self.grid_size - self.padding_size) // 6))) +
                    255 * i / ((self.grid_size - self.padding_size) // 6),
                    int(light_color[2] * (1 - i / ((self.grid_size - self.padding_size) // 6))) +
                    255 * i / ((self.grid_size - self.padding_size) // 6),
                ),
                                 (self.border_size + pos[1] * self.grid_size + self.padding_size // 2 + i,
                                  self.border_size + pos[0] * self.grid_size + self.padding_size // 2 + i,
                                  self.grid_size - self.padding_size - 2 * i,
                                  self.grid_size - self.padding_size - 2 * i),
                                 0)

    def draw_final_territory(self, scr):
        """
        显示最终领地（游戏结束后）
        :param scr: 屏幕
        :return:
        """
        for pos in self.blue_final_territory:
            pygame.draw.rect(
                surface=scr,
                color=[int(255 - (255 - i) * 0.4) for i in self.BLUE],
                rect=(self.border_size + pos[1] * self.grid_size + self.padding_size // 2,
                      self.border_size + pos[0] * self.grid_size + self.padding_size // 2,
                      self.grid_size - self.padding_size,
                      self.grid_size - self.padding_size),
            )

        for pos in self.green_final_territory:
            pygame.draw.rect(
                surface=scr,
                color=[int(255 - (255 - i) * 0.4) for i in self.GREEN],
                rect=(self.border_size + pos[1] * self.grid_size + self.padding_size // 2,
                      self.border_size + pos[0] * self.grid_size + self.padding_size // 2,
                      self.grid_size - self.padding_size,
                      self.grid_size - self.padding_size),
            )

    def draw_wall(self, scr):
        """
        绘制墙
        :param scr: 屏幕
        :return:
        """
        for i in range(self.board_len):
            for j in range(self.board_len):
                if self.board.state[6, i, j] == 1:
                    self.draw_horizontal_wall(scr, self.WHITE, i, j)
                if self.board.state[9, i, j] == 1:
                    self.draw_vertical_wall(scr, self.WHITE, i, j)


    def draw_horizontal_wall(self, scr, color, pos_y, pos_x, width=0):
        """
        绘制水平墙
        :param scr: 屏幕
        :param color: 颜色
        :param pos_y: 纵坐标
        :param pos_x: 横坐标
        :param width: 外框宽度 0为填充
        :return:
        """
        pygame.draw.polygon(
            surface=scr,
            color=color,
            points=((self.border_size + pos_x * self.grid_size,
                     self.border_size + (pos_y + 1) * self.grid_size),
                    (self.border_size + pos_x * self.grid_size + self.padding_size // 4,
                     self.border_size + (pos_y + 1) * self.grid_size + self.padding_size // 4),
                    (self.border_size + (pos_x + 1) * self.grid_size - self.padding_size // 4,
                     self.border_size + (pos_y + 1) * self.grid_size + self.padding_size // 4),
                    (self.border_size + (pos_x + 1) * self.grid_size,
                     self.border_size + (pos_y + 1) * self.grid_size),
                    (self.border_size + (pos_x + 1) * self.grid_size - self.padding_size // 4,
                     self.border_size + (pos_y + 1) * self.grid_size - self.padding_size // 4),
                    (self.border_size + pos_x * self.grid_size + self.padding_size // 4,
                     self.border_size + (pos_y + 1) * self.grid_size - self.padding_size // 4),
                    ),
            width=width
        )


    def draw_vertical_wall(self, scr, color, pos_y, pos_x, width=0):
        """
        绘制垂直墙
        :param scr: 屏幕
        :param color: 颜色
        :param pos_y: 纵坐标
        :param pos_x: 横坐标
        :param width: 外框宽度 0为填充
        :return:
        """
        pygame.draw.polygon(
            surface=scr,
            color=color,
            points=((self.border_size + (pos_x + 1) * self.grid_size,
                     self.border_size + pos_y * self.grid_size),
                    (self.border_size + (pos_x + 1) * self.grid_size + self.padding_size // 4,
                     self.border_size + pos_y * self.grid_size + self.padding_size // 4),
                    (self.border_size + (pos_x + 1) * self.grid_size + self.padding_size // 4,
                     self.border_size + (pos_y + 1) * self.grid_size - self.padding_size // 4),
                    (self.border_size + (pos_x + 1) * self.grid_size,
                     self.border_size + (pos_y + 1) * self.grid_size),
                    (self.border_size + (pos_x + 1) * self.grid_size - self.padding_size // 4,
                     self.border_size + (pos_y + 1) * self.grid_size - self.padding_size // 4),
                    (self.border_size + (pos_x + 1) * self.grid_size - self.padding_size // 4,
                     self.border_size + pos_y * self.grid_size + self.padding_size // 4),
                    ),
            width=width)

    def mouse_pos_to_action(self, mouse_pos):
        """
        将鼠标位置转换为动作
        :param mouse_pos: 鼠标位置
        :return: 动作（0-99整数）
        """
        x, y = mouse_pos
        grid = (y - self.border_size) // self.grid_size, (x - self.border_size) // self.grid_size

        active_pos = self.board.player_pos[int(self.board.state[12, 0, 0])]

        move = grid[0] - active_pos[0], grid[1] - active_pos[1]

        internal_x = (x - self.border_size) % self.grid_size
        internal_y = (y - self.border_size) % self.grid_size

        if internal_x > internal_y:
            wall = 3 if internal_x > self.grid_size - internal_y else 0
        else:
            wall = 2 if internal_x > self.grid_size - internal_y else 1

        try:
            action = self.board.pos_to_action[move] * 4 + wall
        except KeyError:
            return None

        return action

    def do_action(self, action):
        """
        执行动作
        :param action: 动作（0-99整数）
        :return:
        """
        if action not in self.board.available_actions:
            return
        self.board.do_action(action)
        self.history.append(action)

        if self.board.is_game_over_()[0]:
            self.running = False

            self.blue_final_territory = self.board.is_game_over_()[1]
            self.green_final_territory = self.board.is_game_over_()[2]

            self.all_games.append(self.history)
            self.history = []

            self.print_result()

        self.active_player_pos_index = 0 if self.board.state[12, 0, 0] == 0 else 3
        self.active_player_color = self.BLUE if self.board.state[12, 0, 0] == 0 else self.GREEN

    def print_result(self):
        """
        打印游戏结果
        :return:
        """
        blue_score = len(self.board.is_game_over_()[1])
        green_score = len(self.board.is_game_over_()[2])

        print(f"BLUE:{blue_score}, GREEN:{green_score}")

        if blue_score > green_score:
            print("BLUE WIN!")
        elif blue_score < green_score:
            print("GREEN WIN!")
        else:
            print("DRAW!")

    def save_games(self):
        if not self.all_games:
            print("No self saved")
            return

        os.makedirs('./log/board', exist_ok=True)

        t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        with open(f'./log/board/match_history_{t}.json', 'w', encoding='utf-8') as f:
            json.dump(self.all_games, f)

        print(f"Saved {len(self.all_games)} games to ./log/games")

    def init_screen(self):
        """
        初始化屏幕
        :return: 屏幕对象
        """
        screen = pygame.display.set_mode((self.window_size, self.window_size))
        ico = pygame.image.load('../resources/icon/bluegreen.png')
        pygame.display.set_icon(ico)
        pygame.display.set_caption('围城')
        return screen

    def reset(self):
        """
        重置游戏
        :return:
        """
        self.board.clear_board()
        self.running = True
        self.active_player_pos_index = 0
        self.active_player_color = self.BLUE
        self.blue_final_territory = []
        self.green_final_territory = []
        self.history = []

    def robot_handler(self):
        """
        机器人管理器
        :return:
        """
        if self.running and self.robots[int(self.board.state[12, 0, 0])] is not None:
            action = self.robots[int(self.board.state[12, 0, 0])].play()
            self.do_action(action)

    def event_handler(self):
        """
        事件管理器
        :return:
        """
        events = pygame.event.get()
        for event in events:
            # 退出
            if event.type == QUIT:
                self.save_games()
                pygame.display.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.running:
                self.do_action(self.mouse_pos_to_action(pygame.mouse.get_pos()))
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.reset()

    def main(self):
        """
        主函数
        :return:
        """
        pygame.init()
        screen = self.init_screen()

        while True:
            self.event_handler()
            self.robot_handler()
            self.display(screen)

            pygame.display.update()


if __name__ == '__main__':
    game = Game(7, 100, 50, 24,
                (None, (MaxTolerantPercentSigmoidTerritory, {"K": 2, "B": 2, "error": 0.0, "T": 0.03})))
    game.main()
