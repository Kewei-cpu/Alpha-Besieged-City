import json

import pygame

from alphazero import ChessBoard

action_to_pos = {
    0: (-3, 0),
    1: (-2, -1), 2: (-2, 0), 3: (-2, 1),
    4: (-1, -2), 5: (-1, -1), 6: (-1, 0), 7: (-1, 1), 8: (-1, 2),
    9: (0, -3), 10: (0, -2), 11: (0, -1), 12: (0, 0), 13: (0, 1), 14: (0, 2), 15: (0, 3),
    16: (1, -2), 17: (1, -1), 18: (1, 0), 19: (1, 1), 20: (1, 2),
    21: (2, -1), 22: (2, 0), 23: (2, 1),
    24: (3, 0)
}
# load data
path = "../log/hist/games.json"
with open(path, 'r') as f:
    games = json.load(f)

last_game = games[123]

board = ChessBoard()

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if len(last_game) > 0:
                action = last_game.pop(0)
                board.do_action(action)

    screen.fill((255, 255, 255))

    width = 85

    for i in range(7):
        for j in range(7):
            pygame.draw.rect(screen, (0, 0, 0), (100 + i * width, 100 + j * width, width, width), 1)

    X_pos = board.state[0]
    O_pos = board.state[3]

    for i in range(7):
        for j in range(7):
            if X_pos[j, i] == 1:
                pygame.draw.circle(screen, (0, 0, 255), (100 + i * width + width // 2, 100 + j * width + width // 2),
                                   width // 2 - 10)
            if O_pos[j, i] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (100 + i * width + width // 2, 100 + j * width + width // 2),
                                   width // 2 - 10)

    horizontal_wall = board.state[6]
    vertical_wall = board.state[9]

    for i in range(7):
        for j in range(7):
            if horizontal_wall[j, i] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (100 + i * width, 100 + j * width + width, width, 10))
            if vertical_wall[j, i] == 1:
                pygame.draw.rect(screen, (0, 0, 0), (100 + i * width + width, 100 + j * width, 10, width))

    # if board.is_game_over()[0]:
    #     break

    pygame.display.update()
