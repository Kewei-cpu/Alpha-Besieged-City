import json

import matplotlib.pyplot as plt
import numpy as np

# load data
with open("../log/hist/train_losses.json", 'r') as f:
    losses1 = json.load(f)

with open("../log/history/train_losses.json", 'r') as f:
    losses2 = json.load(f)



# plot data
x = np.array([loss[1] for loss in losses1] + [loss[1] for loss in losses2])
# y = np.array([loss[1] for loss in losses])

plt.plot(x, )
plt.xlabel('iterations')
plt.ylabel('loss')
plt.title('loss history')
plt.show()
