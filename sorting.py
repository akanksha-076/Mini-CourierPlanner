"""
sorting.py
Phase 2 (part 1): Parcel prioritization using Merge Sort.
Time complexity: O(n log n) in all cases. Space: O(n).
"""


def merge_sort(items, key):
    """Sort a list using merge sort.

    items : list of items to sort
    key   : function that gives the value to compare for each item
    Merge sort is stable: items with equal keys keep their original order.
    """
    # Base case: a list of 0 or 1 items is already sorted
    if len(items) <= 1:
        return items

    # Divide: split the list into two halves and sort each half recursively
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)

    # Conquer: merge the two sorted halves into one sorted list
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        # Take the smaller item first (<= keeps the sort stable)
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add whatever is left in either half
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def sort_parcels(parcels):
    """Prioritize parcels: earliest deadline first.
    If two parcels have the same deadline, the higher value comes first
    (the minus sign on value reverses its order).
    """
    return merge_sort(parcels, key=lambda p: (p["deadline"], -p["value"]))