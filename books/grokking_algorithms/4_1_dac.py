"""
Divide and Conquer.
Dziel i rzadz.
"""
#%%
def summ(arr):
    """Sum array using recursion."""
    if len(arr) == 1:
        return arr[0]
    else:
        return arr[0] + summ(arr[1:])


assert summ([1, 4, 3, 4, 1]) == 13


def countt(arr):
    """Count elements in a array."""
    if len(arr) == 1:
        return 1
    else:
        return 1 + countt(arr[1:])

assert countt([1, 5, 3, 2, 2]) == 5


def maxx(arr):
    """Biggest element in a array."""
    if len(arr) == 1:
        return arr[0]
    else:
        xn = maxx(arr[1:])
        if arr[0] > xn:
            return arr[0]
        else:
            return xn

assert maxx([10, 5, 2, 7, 1]) == 10


#%% Binary search (recurrence case)
def binary_search(arr, p, r, target):
    if p == r:
        if arr[p] == target:
            return True
        else:
            return False
    else:
        q = (p+r) // 2
        if arr[q] >= target:
            return binary_search(arr, p, q, target)
        elif arr[q] < target:
            return binary_search(arr, q+1, r, target)


# TEST
assert binary_search([1,2,3,4,5], 0, 5, 3) is True
assert binary_search([1,2,3,5,6], 0, 5, 4) is False
