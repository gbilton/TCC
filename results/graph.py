import matplotlib.pyplot as plt
import numpy as np


scores = np.load("results/scores.npy")

scores = [score for i, score in enumerate(scores) if score > -200 and i <= 4000]
running_average = []
for i, score in enumerate(scores):
    lower_limit = i - 100
    if lower_limit < 0:
        lower_limit = 0
    running_average.append(np.average(scores[lower_limit:i]))


plt.plot(scores, label="Resultado dos episódios")
plt.plot(running_average, color="red", label="Média dos últimos 100 episódios")
plt.title("Resultados durante a fase de treinamento")
plt.xlabel("Episódios")
plt.ylabel("Performance")
plt.legend()
plt.show()
