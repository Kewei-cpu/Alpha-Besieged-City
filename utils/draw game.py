import json

import pygame

from alphazero import ChessBoard
from copy import deepcopy

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
path = "../log/games.json"
with open(path, 'r') as f:
    games = json.load(f)

game_index = 1300

game = games[game_index].copy()

board = ChessBoard()

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess")

move_count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(game) > 0:
                    action = game.pop(0)
                    board.do_action(action)
                    move_count += 1
            elif event.key == pygame.K_LEFT:
                game_index -= 1
                game = games[game_index].copy()
                board = ChessBoard()
                move_count = 0
            elif event.key == pygame.K_RIGHT:
                game_index += 1
                game = games[game_index].copy()
                board = ChessBoard()
                move_count = 0

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

    # show game index
    font = pygame.font.SysFont("Microsoft YaHei", 30)
    text = font.render(f"Game {game_index}   Move {move_count}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = 400
    text_rect.centery = 50
    screen.blit(text, text_rect)

    if board.is_game_over()[0]:
        winner = "Blue" if board.is_game_over()[1] == 0 else "Red"
        text = font.render(f"Game Over  {winner} Wins", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = 400
        text_rect.centery = 750
        screen.blit(text, text_rect)


    # if board.is_game_over()[0]:
    #     break

    pygame.display.update()
