# %%
import json
import os
import time

import matplotlib.pyplot as plt
import numpy as np

from arena import *

# r = [MaxSigmoidTerritory] * 3 + [MaxTerritory] + [MaxDictTerritory] * 2 + [MaxPercentSigmoidTerritory] * 3
# p = [
#     {"name": "Max 2x+2", "K": 2, "B": 2},
#     {"name": "Max 2x+1", "K": 2, "B": 1},
#     {"name": "Max 3x+1", "K": 3, "B": 1},
#     {"name": "Max 0/0.5/1"},
#     {"name": "Max 0.2/0.5/0.8/1", "D": {0: 0.2, -1: 0.5, -2: 0.8, -3: 1}},
#     {"name": "Max 0.1/0.3/0.7/1", "D": {0: 0.1, -1: 0.3, -2: 0.7, -3: 1}},
#     {"name": "MaxRel 2x+2", "K": 2, "B": 2},
#     {"name": "MaxRel 2x+1", "K": 2, "B": 1},
#     {"name": "MaxRel 3x+1", "K": 3, "B": 1},
# ]

# r = [MaxPercentSigmoidTerritory] * 2
# p = [{"name": "MaxRel 2x+1", "K": 2, "B": 1},
#      {"name": "MaxRel 3x+1", "K": 3, "B": 1}, ]

if __name__ == "__main__":

    r = [MaxPercentSigmoidTerritory, Random]
    p = [{'K': 2, 'B': 2, 'error': 0.0}, {}]

    arena = Arena(robots=r, param_list=p)
    history = arena.match(N=25000, elo=False)

    os.makedirs('../log/arena', exist_ok=True)

    t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    with open(f'../log/arena/match_history_{t}.json', 'w', encoding='utf-8') as f:
        json.dump(history, f)

    print("=" * 60)
    print("NAME                   ELO           WIN-DRAW-LOSE")
    print("=" * 60)

    plt.figure(figsize=(12, 8))

    for robot in arena.robots:
        print(
            f"{robot.name:<20}{str(round(robot.elo, 1)):>6} {str(round(np.mean(robot.elos), 1)):>6}      {robot.results.count(1)}-{robot.results.count(0.5)}-{robot.results.count(0)}")
        x = np.arange(len(robot.elos))
        y = np.array([np.mean(robot.elos[:i + 1]) for i in x])
        plt.plot(x, y, label=robot.name)
    plt.legend()
    plt.xlabel("Game")
    plt.ylabel("ELO")
    plt.show()
