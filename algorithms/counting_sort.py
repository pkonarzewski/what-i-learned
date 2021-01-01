#%%
def counting_sort(input, k):
    """
    input - input array of non negative integers
    k - range of key values
    """
    c = [0 for _ in range(k)]  # O(k)
    output = [None for _ in range(len(input))]  # O(n)

    for num in input:  # O(n)
        c[num] += 1

    for i in range(1, len(c)):  # O(k)
        c[i] += c[i - 1]

    for num in reversed(input):  # O(n)
        output[c[num] - 1] = num
        c[num] -= 1

    return output


counting_sort([5, 3, 6, 7, 8, 2, 1, 3, 6, 3, 3, 5], k=9)

# %%
