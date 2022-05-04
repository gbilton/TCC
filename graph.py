import matplotlib.pyplot as plt
import numpy as np


scores = np.load("scores.npy")
print(scores)
plt.plot(scores)
plt.show()
