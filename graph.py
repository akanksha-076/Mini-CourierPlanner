"""
graph.py
Phase 3 (part 1): Graph building and Dijkstra's shortest path algorithm.
Dijkstra with a min-heap: O((V + E) log V)
"""

import heapq   # heapq gives us a priority queue (min-heap)


def build_graph(edges):
    """Build an adjacency list from a list of edges [u, v, distance].
    Roads are two-way, so each edge is added in both directions.
    Result looks like: {0: [(1, 4), (2, 2)], 1: [(0, 4), ...], ...}
    """
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))
    return graph


def dijkstra(graph, source):
    """Find the shortest distance from the source to every other node.

    Returns:
      dist : shortest distance to each node
      prev : the previous node on the shortest path (used to rebuild paths)
    """
    # Start by assuming every node is infinitely far away
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0

    # The heap always gives us the closest unvisited node first
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)

        # Skip outdated entries (we already found a shorter way to u)
        if d > dist[u]:
            continue

        # Relaxation: check if going through u gives a shorter path to v
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, prev


def get_path(prev, target):
    """Rebuild the shortest path to the target by following 'prev' backwards."""
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    return path[::-1]   # reverse so the path starts at the source