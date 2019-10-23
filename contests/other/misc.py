#%%
"""
Given a list of numbers and a number k, return whether any two numbers from the list add up to k.
For example, given[10, 15, 3, 7] and k of 17, return true since 10 + 7 is 17.
by Google
"""

arr: list = [10, 15, 3, 7]
k: int = 20


def test_sum(arr: list, k: int):
    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j and arr[i]+arr[j] == k:
                return True
    return False


assert test_sum([10, 15, 3, 7], 17) is True
print(test_sum(arr, k))


#%%
