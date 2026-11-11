"""
main.py
Runs the full courier planning pipeline on the sample dataset:
load data -> sort parcels -> knapsack -> Dijkstra -> nearest-neighbor route.
"""

import json
from sorting import sort_parcels
from knapsack import knapsack, print_dp_table
from graph import build_graph, dijkstra, get_path
from tsp import nearest_neighbor_route

# ---------- Load the dataset ----------
# small.json holds the vehicle capacity, the parcels and the road edges
with open("data/small.json") as f:
    data = json.load(f)

# ---------- Phase 2: Prioritization and box filling ----------
# Step 1: sort parcels by deadline (earliest first), then by value
sorted_parcels = sort_parcels(data["parcels"])
print("Sorted parcels:")
for p in sorted_parcels:
    print(" ", p)

# Step 2: use knapsack DP to pick the best parcels for one trip
best_value, selected, dp = knapsack(sorted_parcels, data["capacity"])
print("\nDP table:")
print_dp_table(dp)
print("\nBest total value:", best_value)
print("Selected parcels:", [p["id"] for p in selected])
print("Total weight:", sum(p["weight"] for p in selected))

# ---------- Phase 3: Route maker and graph processing ----------
# Step 3: build the road network and find shortest paths from the depot (node 0)
graph = build_graph(data["edges"])
print("\nShortest paths from depot (0):")
dist, prev = dijkstra(graph, 0)
for node in sorted(graph):
    print(f"  0 -> {node}: distance {dist[node]}, path {get_path(prev, node)}")

# Step 4: the delivery stops are the destinations of the selected parcels
# (a set removes duplicates if two parcels go to the same place)
stops = list({p["destination"] for p in selected})

# Step 5: order the stops using nearest-neighbor and calculate the route length
route, full_path, total = nearest_neighbor_route(graph, 0, stops)
print("\nDelivery order:", route)
print("Full road path:", full_path)
print("Total route length:", total)