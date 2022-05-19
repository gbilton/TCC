import matplotlib.pyplot as plt
import numpy as np


scores = np.load("results/losses.npy")

scores = [score for i, score in enumerate(scores)]

plt.plot(scores)
plt.show()
