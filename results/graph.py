import matplotlib.pyplot as plt
import numpy as np


scores = np.load("results/scores.npy")

scores = [score for i, score in enumerate(scores) if score > -200]

plt.plot(scores)
plt.show()
