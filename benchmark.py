"""
benchmark.py
Phase 4: Performance testing.
Measures the runtime of sorting, knapsack, Dijkstra and TSP on datasets of
increasing size and saves a runtime chart.
"""

import random
import time
import matplotlib.pyplot as plt
from sorting import sort_parcels
from knapsack import knapsack
from graph import build_graph, dijkstra
from tsp import nearest_neighbor_route


def make_data(n):
    """Create a random dataset with n parcels and a connected road network."""
    parcels = [{"id": f"P{i}",
                "weight": random.randint(1, 10),
                "value": random.randint(10, 100),
                "deadline": random.randint(1, 10),
                "destination": random.randint(1, n)} for i in range(n)]

    # A chain of roads 0-1-2-...-n guarantees every node can be reached
    edges = [[i, i + 1, random.randint(1, 20)] for i in range(n)]
    # Extra random roads make the network more realistic
    edges += [[random.randint(0, n), random.randint(0, n), random.randint(1, 20)]
              for _ in range(n * 2)]
    return parcels, edges


# Dataset sizes to test, and a place to store the time of each step
sizes = [10, 50, 100, 200, 400]
times = {"Sorting": [], "Knapsack": [], "Dijkstra": [], "TSP": []}

for n in sizes:
    parcels, edges = make_data(n)
    graph = build_graph(edges)

    # Time the sorting step
    t = time.perf_counter()
    s = sort_parcels(parcels)
    times["Sorting"].append(time.perf_counter() - t)

    # Time the knapsack step (vehicle capacity fixed at 100)
    t = time.perf_counter()
    _, sel, _ = knapsack(s, 100)
    times["Knapsack"].append(time.perf_counter() - t)

    # Time one Dijkstra run from the depot
    t = time.perf_counter()
    dijkstra(graph, 0)
    times["Dijkstra"].append(time.perf_counter() - t)

    # Time the TSP route on the destinations of the selected parcels
    stops = list({p["destination"] for p in sel})
    t = time.perf_counter()
    nearest_neighbor_route(graph, 0, stops)
    times["TSP"].append(time.perf_counter() - t)

    # Print the times for this dataset size (used as screenshot evidence)
    print(n, {k: round(v[-1], 5) for k, v in times.items()})

# ---------- Draw and save the runtime chart ----------
for name, vals in times.items():
    plt.plot(sizes, vals, marker="o", label=name)
plt.xlabel("Number of parcels / nodes")
plt.ylabel("Runtime (seconds)")
plt.title("Runtime of major steps")
plt.legend()
plt.savefig("runtime_chart.png")   # saved in the project folder
plt.show()