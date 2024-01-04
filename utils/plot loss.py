import json

import matplotlib.pyplot as plt
import numpy as np

# load data
with open("../log/2024-1-3-history/train_losses.json", 'r') as f:
    losses = json.load(f)

with open("../log/train_losses.json", 'r') as f:
    losses += json.load(f)



# plot data
x = np.array([loss[1] for loss in losses])
# y = np.array([loss[1] for loss in losses])

plt.plot(x, )
plt.xlabel('iterations')
plt.ylabel('loss')
plt.title('loss history')
plt.show()
