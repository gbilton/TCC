import matplotlib.pyplot as plt
import numpy as np


scores = np.load("results/scores.npy")

scores = [score for i, score in enumerate(scores) if score > -200]
print(scores)

plt.plot(scores)
plt.show()
