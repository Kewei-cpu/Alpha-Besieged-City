import matplotlib.pyplot as plt
import numpy as np

win_rate = np.array([float(x) for x in "1 1 0.7 0 0 0 0 0.6 1 0.7 0 0 1 0 0 1 0 0 0 1 1 0.4 0 0 1 0 0.8 1".split(' ')])

cumulated_win_rate = np.cumsum(win_rate) / np.arange(1, len(win_rate) + 1)

iteration = np.arange(len(win_rate) * 100, step=100)


plt.plot(iteration, win_rate, 'o-')
plt.xlabel('iterations')
plt.ylabel('win_rate')

plt.show()
