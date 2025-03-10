"""
Selection sort.
Sortowanie przez wybieranie.
"""
#%%

def selection_sort(array):
    """Serach for a smallest value and insert into new array."""

    arr = array.copy()
    sorted_array = []

    while len(arr) > 0:
        min_pos = 0

        for n in range(len(arr)):
            if arr[n] < arr[min_pos]:
                min_pos = n

        sorted_array.append(arr.pop(min_pos))

    return sorted_array


def selection_sort2(arr):
    n = len(arr)

    for i in range(n - 1):
        min_pos = i

        for j in range(i+1, n):
            if arr[j] < arr[min_pos]:
                min_pos = j

        old = arr[i]
        new = arr[min_pos]
        arr[i] = new
        arr[min_pos] = old
    return arr


#%%
# TEST
assert selection_sort([101, 5, 4, 3, 6, 2, 3]) == [2, 3, 3, 4, 5, 6, 101]
assert selection_sort([4, 4, 2, 2, 1, 3]) == [1, 2, 2, 3, 4, 4]

assert selection_sort2([101, 5, 4, 3, 6, 2, 3]) == [2, 3, 3, 4, 5, 6, 101]
assert selection_sort2([4, 4, 2, 2, 1, 3]) == [1, 2, 2, 3, 4, 4]
