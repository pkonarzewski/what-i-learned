#%%
def selection_sort(arr):
    """Selection sort."""
    for i in range(len(arr)):
        min_val_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_val_index]:
                min_val_index = j
        arr[i], arr[min_val_index] = arr[min_val_index], arr[i]

    return arr

input_arr = [1, 4, 7, 2, 44, 7, 3, 21, 3]
print(selection_sort(input_arr))
assert selection_sort(input_arr) == sorted(input_arr)
