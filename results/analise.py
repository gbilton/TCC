import pickle
import matplotlib.pyplot as plt


def main():
    with open("results/results", "rb") as f:
        results = pickle.load(f)

    graph_1 = {
        "data": [],
        "x_label": "Number of Vehicles",
        "y_label": "Score",
        "title": "Gráfico 1",
    }
    for result in results:
        graph_1["data"].append(
            {
                "score": result["score"],
                "number of cars": result["number of cars"],
                "method": result["method"],
            }
        )

    number_of_cars = sorted(list(set([result["number of cars"] for result in results])))
    methods = sorted(list(set([result["method"] for result in results])))

    graph_2 = {
        "data": [],
        "x_label": "Number of Vehicles",
        "y_label": "Score",
        "title": "Gráfico 2",
    }
    for n in number_of_cars:
        for m in methods:
            scores = []
            for d in results:
                if d["number of cars"] == n and d["method"] == m:
                    scores.append(d["score"])
            avg_score = sum(scores) / len(scores)
            graph_2["data"].append(
                {
                    "score": avg_score,
                    "number of cars": n,
                    "method": m,
                }
            )

    graphs = [graph_1, graph_2]
    color_map = {
        "random_action": "blue",
        "select_action": "green",
        "formal_action": "red",
    }
    for i, graph in enumerate(graphs):
        plt.figure(i)
        methods = sorted(list(set([data["method"] for data in graph["data"]])))
        for method in methods:
            x = [point["number of cars"] for point in graph["data"] if point["method"] == method]
            y = [point["score"] for point in graph["data"] if point["method"] == method]
            color = color_map[method]
            plt.scatter(x, y, color=color, label=method)
        plt.legend()
        plt.xlabel(graph["x_label"])
        plt.ylabel(graph["y_label"])
        plt.title(graph["title"])

    plt.show()


if __name__ == "__main__":
    main()
