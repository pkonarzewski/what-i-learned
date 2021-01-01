#%%
def insertion_sort(arr):
    """Insertion sort."""
    for i in range(1, len(arr)):  # O(n)
        key = arr[i]

        j = i - 1
        while key < arr[j] and j >= 0:  # O(n)
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


insertion_sort([8, 8, 1, 5, 3, 2, 1, 9, 6])
