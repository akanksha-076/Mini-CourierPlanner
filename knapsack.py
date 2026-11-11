"""
knapsack.py
Phase 2 (part 2): Packing plan using 0/1 Knapsack (Dynamic Programming).
Time complexity: O(n * C), Space: O(n * C)
n = number of parcels, C = vehicle capacity.
"""


def knapsack(parcels, capacity):
    """Choose the set of parcels with the highest total value that fits
    within the capacity. Each parcel is either taken or left (0/1).

    Returns: (best total value, list of selected parcels, the DP table)
    """
    n = len(parcels)

    # dp[i][c] = best value using the first i parcels with capacity c.
    # Row 0 and column 0 stay 0 (no parcels or no capacity = no value).
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Fill the table one parcel at a time
    for i in range(1, n + 1):
        w = parcels[i - 1]["weight"]   # weight of the current parcel
        v = parcels[i - 1]["value"]    # value of the current parcel
        for c in range(capacity + 1):
            # Option 1: skip this parcel (value stays as in the row above)
            dp[i][c] = dp[i - 1][c]
            # Option 2: take this parcel, if it fits in the current capacity
            if w <= c:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    # Backtracking: walk back through the table to find which parcels were taken
    selected, c = [], capacity
    for i in range(n, 0, -1):
        # If the value changed compared to the row above, this parcel was taken
        if dp[i][c] != dp[i - 1][c]:
            selected.append(parcels[i - 1])
            c -= parcels[i - 1]["weight"]   # reduce the remaining capacity
    selected.reverse()                      # restore the original order

    return dp[n][capacity], selected, dp


def print_dp_table(dp):
    """Print the DP table row by row (used as Phase 2 evidence)."""
    for row in dp:
        print(" ".join(f"{x:3}" for x in row))