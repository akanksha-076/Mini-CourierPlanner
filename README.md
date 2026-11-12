# Intelligent Courier Planning System

A Python prototype that takes a list of parcels and delivery points, then produces a **prioritized parcel list**, an **optimal packing plan** and an **ordered delivery route**. It combines sorting, dynamic programming, graph algorithms and an approximation technique into one integrated application.

- **Author:** Akanksha Kumari
- **Roll No.:** 2501010076
- **University:** K. R. Mangalam University, Gurugram, Haryana
- **Course:** Design & Analysis of Algorithms (ETCCDA302)
- **Faculty:** Ankita Gupta
- **Assignment** (Capstone Assignment): Mini-Courier Planner
- **GitHub:** https://github.com/akanksha-076
---

## 1. Problem Statement

A courier has a vehicle with limited capacity and many parcels to deliver. The system must:

1. Decide which parcels are most urgent.
2. Choose the best set of parcels for one trip without exceeding the vehicle capacity.
3. Find the shortest road distance between delivery points.
4. Decide the order in which to visit the customers and return to the depot.
5. Measure how fast each part of the system runs.

---

## 2. Algorithms Used

| Step | Algorithm | Why this algorithm | Time complexity |
|------|-----------|--------------------|-----------------|
| Parcel prioritization | Merge Sort | Stable and always O(n log n) | O(n log n) |
| Packing plan | 0/1 Knapsack (Dynamic Programming) | Gives the optimal parcel set under a capacity limit | O(n × C) |
| Shortest paths | Dijkstra's Algorithm (min-heap) | Road distances are non-negative | O((V + E) log V) |
| Delivery route | Nearest-Neighbor TSP approximation | Exact TSP is NP-hard, so a fast heuristic is used | O(k × (V + E) log V) |

*n = number of parcels, C = vehicle capacity, V = nodes, E = edges, k = number of delivery stops.*

---

## 3. System Flow

```
Load data (JSON)
      |
Sort parcels (deadline first, then value)
      |
Knapsack DP -> selected parcels for the trip
      |
Extract delivery destinations
      |
Build graph -> Dijkstra shortest paths
      |
Nearest-Neighbor TSP -> final route + total distance
      |
Benchmark runtime of every step
```

---

## 4. Data Design

### Parcel attributes

| Field | Meaning |
|-------|---------|
| `id` | Unique parcel ID (e.g. P1) |
| `weight` | Parcel weight in kg (used as knapsack weight) |
| `value` | Priority score (used as knapsack value) |
| `deadline` | Days left to deliver (used for sorting) |
| `destination` | Customer node number in the graph |

### Graph format

- Node `0` is the **depot**. Nodes `1, 2, 3...` are **customers**.
- Edges are two-way roads written as `[node_a, node_b, distance]`.
- Stored as an adjacency list: `{node: [(neighbor, distance), ...]}`.

### Sample dataset (`data/small.json`)

The file contains the vehicle `capacity`, a list of `parcels` and a list of `edges`.

---

## 5. Project Structure

```
courier_planner/
|-- data/
|   |-- small.json        # sample dataset
|-- screenshots/          # output screenshots
|-- sorting.py            # merge sort + parcel prioritization
|-- knapsack.py           # 0/1 knapsack DP + backtracking
|-- graph.py              # graph builder + Dijkstra
|-- tsp.py                # nearest-neighbor route planner
|-- main.py               # runs the full pipeline
|-- benchmark.py          # runtime testing and chart
|-- runtime_chart.png     # generated runtime chart
|-- README.md
```

---

## 6. How to Run

### Requirements

- Python 3.8 or higher
- matplotlib (only for the runtime chart)

### Steps

1. Clone or download the project:
   ```
   git clone https://github.com/akanksha-076/Mini-CourierPlanner.git
   cd Mini-CourierPlanner
   ```
2. Install the chart library:
   ```
   pip install matplotlib
   ```
3. Run the full courier system on the sample dataset:
   ```
   python main.py
   ```
4. Run the performance tests and generate the runtime chart:
   ```
   python benchmark.py
   ```

---

## 7. Sample Output

```
Sorted parcels:
  {'id': 'P2', 'weight': 4, 'value': 50, 'deadline': 1, 'destination': 2}
  {'id': 'P4', 'weight': 5, 'value': 60, 'deadline': 2, 'destination': 4}
  {'id': 'P1', 'weight': 3, 'value': 40, 'deadline': 2, 'destination': 1}
  {'id': 'P3', 'weight': 2, 'value': 30, 'deadline': 3, 'destination': 3}
  {'id': 'P5', 'weight': 1, 'value': 10, 'deadline': 4, 'destination': 5}

DP table:
  0   0   0   0   0   0   0   0   0   0   0
  0   0   0   0  50  50  50  50  50  50  50
  0   0   0   0  50  60  60  60  60 110 110
  0   0   0  40  50  60  60  90 100 110 110
  0   0  30  40  50  70  80  90 100 120 130
  0  10  30  40  50  70  80  90 100 120 130

Best total value: 130
Selected parcels: ['P4', 'P1', 'P3']
Total weight: 10

Shortest paths from depot (0):
  0 -> 0: distance 0, path [0]
  0 -> 1: distance 3, path [0, 2, 1]
  0 -> 2: distance 2, path [0, 2]
  0 -> 3: distance 8, path [0, 2, 1, 3]
  0 -> 4: distance 10, path [0, 2, 1, 3, 4]
  0 -> 5: distance 13, path [0, 2, 1, 3, 4, 5]

Delivery order: [0, 1, 3, 4, 0]
Full road path: [0, 2, 1, 3, 4, 3, 1, 2, 0]
Total route length: 20
```

---

## 8. Performance Testing

`benchmark.py` generates random datasets of 10, 50, 100, 200 and 400 parcels and measures the runtime of sorting, knapsack, Dijkstra and TSP separately. The result is saved as `runtime_chart.png`.

**Observations** :

- Merge sort and Dijkstra stay very fast even for larger inputs.
- Knapsack grows fastest because its table size is n × capacity.
- TSP time depends on the number of stops, since Dijkstra runs once per stop.

---

## 9. Possible Optimizations

- Use a 1D array in knapsack to cut memory from O(n × C) to O(C).
- Precompute the distances between all delivery stops once instead of running Dijkstra repeatedly in the TSP step.
- Improve the nearest-neighbor route with the **2-opt** heuristic.
- Handle multiple trips by running the knapsack again on the remaining parcels.
- Add a real-time traffic factor to the edge weights.

---

## 10. Limitations

- Nearest-neighbor gives a good route but not always the shortest one.
- The system plans one vehicle and one trip at a time.
- Parcel weights are integers, because the DP table needs whole numbers.

---

## 11. Screenshots

All screenshots are in the `screenshots/` folder:

1. `project_structure.png` - folder structure
2. `sorted_parcels.png` - sorted parcel list
3. `dp_table.png` - knapsack DP table
4. `selected_parcels.png` - packing plan
5. `dijkstra_paths.png` - shortest paths from the depot
6. `final_route.png` - delivery order and total distance
7. `benchmark_output.png` - runtime values in the terminal
8. `runtime_chart.png` - runtime comparison chart


---

## 12. Conclusion

The system shows how classic algorithms can work together on one practical problem: sorting decides what is urgent, dynamic programming decides what fits, Dijkstra measures the roads, and the TSP heuristic decides the delivery order.
