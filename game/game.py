import sys

import pygame
from pygame.locals import *

from alphazero import ChessBoard


class Game:
    WHITE = (255, 255, 255)
    BLUE = (130, 175, 214)
    GREEN = (80, 181, 142)

    def __init__(self, grid_num, grid_size, border_size, padding_size):
        """
        :param padding_size: 每个棋盘格的间距
        :param grid_num: 棋盘格数量
        :param grid_size: 棋盘格大小
        :param border_size: 棋盘边缘空白大小
        """
        self.border_size = border_size
        self.grid_size = grid_size
        self.grid_num = grid_num
        self.window_size = grid_num * grid_size + border_size * 2
        self.padding_size = padding_size
        self.step_flag = 0  # 0为移动，1为放置
        self.mouse_pos = (0, 0)
        self.running = True
        self.board = ChessBoard(grid_num)

    def display(self, scr):
        self.draw_background(scr)
        self.draw_board(scr)
        self.draw_players(scr)
        self.draw_active_player(scr)

    def draw_background(self, scr):
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
        for i in range(self.grid_num):
            for j in range(self.grid_num):
                pygame.draw.rect(
                    surface=scr,
                    color=self.WHITE,
                    rect=(game.border_size + j * game.grid_size + game.padding_size // 2 + 3,
                          game.border_size + i * game.grid_size + game.padding_size // 2 + 3,
                          game.grid_size - game.padding_size - 6,
                          game.grid_size - game.padding_size - 6),
                    border_radius=0
                )

    def draw_players(self, scr):
        player_X_pos = self.board.array_to_coordinates(self.board.state[0])[0]
        player_O_pos = self.board.array_to_coordinates(self.board.state[3])[0]

        pygame.draw.circle(
            surface=scr,
            color=self.BLUE,
            center=(game.border_size + (player_X_pos[1] + 0.5) * game.grid_size,
                    game.border_size + (player_X_pos[0] + 0.5) * game.grid_size),
            radius=game.grid_size * 0.3,
        )
        pygame.draw.circle(
            surface=scr,
            color=self.GREEN,
            center=(game.border_size + (player_O_pos[1] + 0.5) * game.grid_size,
                    game.border_size + (player_O_pos[0] + 0.5) * game.grid_size),
            radius=game.grid_size * 0.3,
        )

    def draw_active_player(self, scr):
        pos_index = 0 if self.board.state[12, 0, 0] == 0 else 3
        color = self.BLUE if self.board.state[12, 0, 0] == 0 else self.GREEN
        pos = self.board.array_to_coordinates(self.board.state[pos_index])[0]

        pygame.draw.circle(
            surface=scr,
            color=[int(color * 0.7) for color in color],
            center=(game.border_size + (pos[1] + 0.5) * game.grid_size,
                    game.border_size + (pos[0] + 0.5) * game.grid_size),
            width=5,
            radius=game.grid_size * 0.3,
        )

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            # 退出
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.running:
                    pass
            # if self.step_flag == 0:
            #     res = Player.all_players[self.player_flag].move_to_mouse()
            #     if res:
            #         self.next_step()
            # elif self.step_flag == 1:
            #     res = Player.all_players[self.player_flag].place_at_mouse()
            #     if res:
            #         self.next_step()

    def scr_pos_to_grid(self, pos):
        """
        讲鼠标坐标转化为再网格中的位置
        :param pos:
        :return:
        """
        x = (pos[1] - self.border_size) // self.grid_size
        y = (pos[0] - self.border_size) // self.grid_size
        return x, y

    def move_mouse_handler(self):
        gd = self.scr_pos_to_grid(pygame.mouse.get_pos())
        if 0 <= gd[0] <= self.grid_num - 1 and 0 <= gd[1] <= self.grid_num - 1:
            self.mouse_pos = gd

    def init_screen(self):
        """
        初始化屏幕
        """
        screen = pygame.display.set_mode((self.window_size, self.window_size))
        ico = pygame.image.load('../resources/icon/xo.ico')
        pygame.display.set_icon(ico)
        pygame.display.set_caption('围城')
        return screen

    def main(self):
        pygame.init()
        screen = self.init_screen()

        while True:
            self.event_handler()
            self.display(screen)

            pygame.display.update()


if __name__ == '__main__':
    game = Game(7, 100, 50, 20)
    game.main()
