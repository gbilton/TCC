import pickle
from typing import Any, List
import matplotlib.pyplot as plt


def graph_all(results, x_label, y_label, title):
    graph_1 = {
        "data": [],
        "x_label": x_label,
        "y_label": y_label,
        "title": title,
    }
    for result in results:
        graph_1["data"].append(
            {
                "score": result["score"],
                "number of cars": result["number of cars"],
                "method": result["method"],
            }
        )
    return graph_1


def graph_average(results, x_label, y_label, title):
    number_of_cars = sorted(list(set([result["number of cars"] for result in results])))
    methods = sorted(list(set([result["method"] for result in results])))

    graph_2 = {
        "data": [],
        "x_label": x_label,
        "y_label": y_label,
        "title": title,
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
    return graph_2


def graph(graphs: List[Any]):
    color_map = {
        "random_action": "blue",
        "act": "green",
        "formal_action": "red",
    }
    method_map = {
        "random_action": "Método Aleatório",
        "act": "Método Inteligente",
        "formal_action": "Método Tradicional",
    }

    for i, graph in enumerate(graphs):
        plt.figure(i)
        methods = sorted(list(set([data["method"] for data in graph["data"]])))
        for method in methods:
            x = [point["number of cars"] for point in graph["data"] if point["method"] == method]
            y = [point["score"] for point in graph["data"] if point["method"] == method]
            color = color_map[method]
            plt.scatter(x, y, color=color, label=method_map[method], alpha=0.9)
        plt.legend()
        plt.xlabel(graph["x_label"])
        plt.ylabel(graph["y_label"])
        plt.title(graph["title"])

    plt.show()


def main():
    with open("results/results", "rb") as f:
        results = pickle.load(f)
    level1_results = [result for result in results if result["level"] == "Level1"]
    level2_results = [result for result in results if result["level"] == "Level2"]

    graph_1 = graph_all(
        results=results,
        x_label="Número de veículos por trajetória",
        y_label="Tempo médio (s)",
        title="Comparativo da performance entre métodos para controle semafórico",
    )

    graph_2 = graph_all(
        results=level1_results,
        x_label="Número de veículos por trajetória",
        y_label="Tempo médio (s)",
        title="Comparativo da performance entre métodos para controle semafórico no mapa 1",
    )

    graph_3 = graph_all(
        results=level2_results,
        x_label="Número de veículos por trajetória",
        y_label="Tempo médio (s)",
        title="Comparativo da performance entre métodos para controle semafórico no mapa 2",
    )

    graph_4 = graph_average(
        results=results,
        x_label="Número de veículos por trajetória",
        y_label="Tempo médio (s)",
        title="Média dos resultados",
    )

    graph_5 = graph_average(
        results=level1_results,
        x_label="Número de veículos por trajetória",
        y_label="Tempo médio (s)",
        title="Média dos resultados por método, para o Nível 1",
    )

    graph_6 = graph_average(
        results=level2_results,
        x_label="Número de veículos por trajetória",
        y_label="Tempo médio (s)",
        title="Média dos resultados por método, para o Nível 2",
    )

    graphs = [graph_1, graph_2, graph_3, graph_4, graph_5, graph_6]
    graph(graphs)


if __name__ == "__main__":
    main()
