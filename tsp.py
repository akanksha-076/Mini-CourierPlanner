"""
tsp.py
Phase 3 (part 2): Delivery route using the Nearest-Neighbor TSP approximation.
Exact TSP is NP-hard, so this fast heuristic gives a good (not always best) route.
"""

from graph import dijkstra, get_path


def nearest_neighbor_route(graph, depot, stops):
    """Build a delivery route that starts and ends at the depot.

    graph : adjacency list of the road network
    depot : starting node (node 0)
    stops : list of customer nodes that must be visited

    Returns: (stop order, full road path, total route distance)
    """
    unvisited = set(stops)    # customers still waiting for delivery
    current = depot           # the courier starts at the depot
    route = [depot]           # order of the delivery stops
    full_path = [depot]       # every road node passed through
    total = 0                 # total distance travelled

    while unvisited:
        # Shortest distances from the current location to all nodes
        dist, prev = dijkstra(graph, current)

        # Greedy choice: go to the closest customer not yet visited
        nxt = min(unvisited, key=lambda s: dist[s])

        total += dist[nxt]
        full_path += get_path(prev, nxt)[1:]   # [1:] avoids repeating the start node
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    # After the last delivery, return to the depot
    dist, prev = dijkstra(graph, current)
    total += dist[depot]
    full_path += get_path(prev, depot)[1:]
    route.append(depot)

    return route, full_path, total