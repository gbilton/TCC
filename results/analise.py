import pickle

with open("results/results", "rb") as f:
    results = pickle.load(f)

print(results)
