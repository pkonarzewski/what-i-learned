#%%
def insertion_sort(arr):
    """Insertion sort."""
    for i in range(1, len(arr)):
        j = i - 1

        while arr[j+1] < arr[j] and j >= 0:
            arr[j+1], arr[j] = arr[j], arr[j+1]
            j -= 1

    return arr


insertion_sort([8, 8, 1, 5, 3, 2, 1, 9, 6])
