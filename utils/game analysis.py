import json

with open("../log/2024-1-3-history/games.json", 'r') as f:
    games = json.load(f)

with open("../log/2024-1-4-history/games.json", 'r') as f:
    games += json.load(f)

print(len(games))  # 2835 games

winners = [0, 0, 0]  # blue wins  red wins  draw

blue_1st_move = {}
red_1st_move = {}

for game in games:
    blue_1st_move[game[0]] = blue_1st_move.get(game[0], 0) + 1
    red_1st_move[game[1]] = red_1st_move.get(game[1], 0) + 1

# print(winners)

l1 = sorted(list(blue_1st_move.items()), key=lambda x: x[1], reverse=True)[:10]
l2 = sorted(list(red_1st_move.items()), key=lambda x: x[1], reverse=True)[:10]

print("Top blue openings:")
for item in l1:
    print(item[0], item[1] / len(games))

print("Top red openings:")
for item in l2:
    print(item[0], item[1] / len(games))
