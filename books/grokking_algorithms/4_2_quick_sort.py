#%% quick sort
"""
Quick Sort.
Sortowanie szybkie.
"""

def quicksort(arr):
    """Quick sort algorithm."""
    if len(arr) < 2:
        return arr
    else:
        greater = []
        lesser = []
        pivot = arr[0]

        for x in arr[1:]:
            if x >= pivot:
                greater.append(x)
            else:
                lesser.append(x)

        return quicksort(lesser) + [pivot] + quicksort(greater)


assert quicksort([9, 5, 2, 3, 6, 1, 2]) == [1, 2, 2, 3, 5, 6, 9]
