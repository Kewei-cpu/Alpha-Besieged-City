import json

import matplotlib.pyplot as plt
import numpy as np

# load data
path = "../log/train_losses.json"
with open(path, 'r') as f:
    losses = json.load(f)

# plot data
x = np.array([loss[0] for loss in losses])
y = np.array([loss[1] for loss in losses])

plt.plot(x, y)
plt.xlabel('iterations')
plt.ylabel('loss')
plt.title('loss history')
plt.show()
