import sys

import pygame
from pygame.locals import *

from alphazero import ChessBoard


class Game:
    WHITE = (255, 255, 255)
    BLUE = (130, 175, 214)
    GREEN = (80, 181, 142)
    GREY = (128, 128, 128)
    BLACK = (0, 0, 0)

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
        self.running = True
        self.board = ChessBoard(grid_num)
        self.active_player_pos_index = 0
        self.active_player_color = self.BLUE

    def display(self, scr):
        self.draw_background(scr)
        self.draw_board(scr)
        self.draw_available_positions(scr)
        self.draw_players(scr)
        self.draw_active_player(scr)
        self.draw_action_preview(scr)
        self.draw_wall(scr)

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
                    rect=(game.border_size + j * game.grid_size + game.padding_size // 2,
                          game.border_size + i * game.grid_size + game.padding_size // 2,
                          game.grid_size - game.padding_size,
                          game.grid_size - game.padding_size),
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

    def draw_action_preview(self, scr):
        if self.mouse_pos_to_action(pygame.mouse.get_pos()) not in self.board.available_actions:
            return

        move = self.board.action_to_pos[self.mouse_pos_to_action(pygame.mouse.get_pos()) // 4]
        wall = self.mouse_pos_to_action(pygame.mouse.get_pos()) % 4

        destination = (self.board.array_to_coordinates(self.board.state[self.active_player_pos_index])[0][0] + move[0],
                       self.board.array_to_coordinates(self.board.state[self.active_player_pos_index])[0][1] + move[1])

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
            center=(game.border_size + (destination[1] + 0.5) * game.grid_size,
                    game.border_size + (destination[0] + 0.5) * game.grid_size),
            radius=game.grid_size * 0.3,
        )

    def draw_wall(self, scr):
        for i in range(self.grid_num):
            for j in range(self.grid_num):
                if self.board.state[6, i, j] == 1:
                    self.draw_horizontal_wall(scr, self.WHITE, i, j)
                if self.board.state[9, i, j] == 1:
                    self.draw_vertical_wall(scr, self.WHITE, i, j)

    def draw_available_positions(self, scr):
        available_positions = []
        for action in self.board.available_actions:
            pos = (self.board.action_to_pos[action // 4][0] +
                   self.board.array_to_coordinates(self.board.state[self.active_player_pos_index])[0][0],
                   self.board.action_to_pos[action // 4][1] +
                   self.board.array_to_coordinates(self.board.state[self.active_player_pos_index])[0][1]
                   )
            if pos not in available_positions:
                available_positions.append(pos)

        light_color = [int(255 - (255 - i) * 0.5) for i in self.active_player_color]

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
                                 (game.border_size + pos[1] * game.grid_size + game.padding_size // 2 + i,
                                  game.border_size + pos[0] * game.grid_size + game.padding_size // 2 + i,
                                  game.grid_size - game.padding_size - 2 * i,
                                  game.grid_size - game.padding_size - 2 * i),
                                 0)

    @staticmethod
    def draw_vertical_wall(scr, color, pos_y, pos_x, width=0):
        pygame.draw.polygon(
            surface=scr,
            color=color,
            points=((game.border_size + (pos_x + 1) * game.grid_size,
                     game.border_size + pos_y * game.grid_size),
                    (game.border_size + (pos_x + 1) * game.grid_size + game.padding_size // 4,
                     game.border_size + pos_y * game.grid_size + game.padding_size // 4),
                    (game.border_size + (pos_x + 1) * game.grid_size + game.padding_size // 4,
                     game.border_size + (pos_y + 1) * game.grid_size - game.padding_size // 4),
                    (game.border_size + (pos_x + 1) * game.grid_size,
                     game.border_size + (pos_y + 1) * game.grid_size),
                    (game.border_size + (pos_x + 1) * game.grid_size - game.padding_size // 4,
                     game.border_size + (pos_y + 1) * game.grid_size - game.padding_size // 4),
                    (game.border_size + (pos_x + 1) * game.grid_size - game.padding_size // 4,
                     game.border_size + pos_y * game.grid_size + game.padding_size // 4),
                    ),
            width=width)

    @staticmethod
    def draw_horizontal_wall(scr, color, pos_y, pos_x, width=0):
        pygame.draw.polygon(
            surface=scr,
            color=color,
            points=((game.border_size + pos_x * game.grid_size,
                     game.border_size + (pos_y + 1) * game.grid_size),
                    (game.border_size + pos_x * game.grid_size + game.padding_size // 4,
                     game.border_size + (pos_y + 1) * game.grid_size + game.padding_size // 4),
                    (game.border_size + (pos_x + 1) * game.grid_size - game.padding_size // 4,
                     game.border_size + (pos_y + 1) * game.grid_size + game.padding_size // 4),
                    (game.border_size + (pos_x + 1) * game.grid_size,
                     game.border_size + (pos_y + 1) * game.grid_size),
                    (game.border_size + (pos_x + 1) * game.grid_size - game.padding_size // 4,
                     game.border_size + (pos_y + 1) * game.grid_size - game.padding_size // 4),
                    (game.border_size + pos_x * game.grid_size + game.padding_size // 4,
                     game.border_size + (pos_y + 1) * game.grid_size - game.padding_size // 4),
                    ),
            width=width
        )

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            # 退出
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.do_action()

            # if self.step_flag == 0:
            #     res = Player.all_players[self.player_flag].move_to_mouse()
            #     if res:
            #         self.next_step()
            # elif self.step_flag == 1:
            #     res = Player.all_players[self.player_flag].place_at_mouse()
            #     if res:
            #         self.next_step()

    def mouse_pos_to_action(self, mouse_pos):
        """
        将鼠标位置转换为动作
        :param mouse_pos: 鼠标位置
        :return: 动作
        """
        x, y = mouse_pos
        grid = (y - self.border_size) // self.grid_size, (x - self.border_size) // self.grid_size

        active_pos = self.board.array_to_coordinates(self.board.state[self.active_player_pos_index])[0]

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

    def init_screen(self):
        """
        初始化屏幕
        """
        screen = pygame.display.set_mode((self.window_size, self.window_size))
        ico = pygame.image.load('../resources/icon/xo.ico')
        pygame.display.set_icon(ico)
        pygame.display.set_caption('围城')
        return screen

    def do_action(self):
        action = self.mouse_pos_to_action(pygame.mouse.get_pos())
        if action not in self.board.available_actions:
            return
        self.board.do_action(action)

        self.active_player_pos_index = 0 if self.board.state[12, 0, 0] == 0 else 3
        self.active_player_color = self.BLUE if self.board.state[12, 0, 0] == 0 else self.GREEN

    def gradientRect(self, scr, first_color, second_color, target_rect, direction):
        """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
        colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap

        if direction == 0:  # horizontal
            pygame.draw.line(colour_rect, first_color, (0, 0), (0, 1))  # left colour line
            pygame.draw.line(colour_rect, second_color, (1, 0), (1, 1))  # right colour line
        elif direction == 1:  # vertical
            pygame.draw.line(colour_rect, first_color, (0, 0), (1, 0))  # top colour line
            pygame.draw.line(colour_rect, second_color, (0, 1), (1, 1))  # bottom colour line

        colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
        colour_rect.set_alpha(200)

        scr.blit(colour_rect, target_rect)

    def main(self):
        pygame.init()
        screen = self.init_screen()

        while True:
            self.event_handler()
            self.display(screen)

            pygame.display.update()


if __name__ == '__main__':
    game = Game(7, 100, 50, 24)
    game.main()
