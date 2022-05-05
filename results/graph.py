import matplotlib.pyplot as plt
import numpy as np


scores = np.load("scores.npy")
plt.plot(scores)
plt.show()
