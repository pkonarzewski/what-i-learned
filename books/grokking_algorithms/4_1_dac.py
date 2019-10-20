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
    print(f'[{p}-{r}] {arr[p:r]}')
    if p >= r:
        if arr[p] == target:
            return arr[p]
        else:
            return None
    else:
        q = (p+r) // 2
        print(q)
        if arr[q] <= target:
            return binary_search(arr, q, r, target)
        else:
            return binary_search(arr, p, q-1, target)


# TEST
print(binary_search([1,2,3,4,5], 0, 5, 7))
# assert binary_search([1,2,3,4,5], 0, 5, 3) is True
# assert binary_search([1,2,3,5,6], 0, 5, 4) is False


#%%
import math
print((2+3) //2,
math.ceil((2+3) / 2))

#%%
