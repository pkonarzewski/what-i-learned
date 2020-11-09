#%% 1.
# Show the performance advantage of binary search over linear search by creating
# a list of one million numbers and timing how long it takes the linear_
# contains() and binary_contains() functions defined in this chapter to find
# various numbers in the list.


def linear_contains(search_list, my_number) -> bool:
    for number in search_list:
        if number == my_number:
            return True
    return False


def binary_contains(search_list, my_number) -> bool:
    low: int = 0
    high: int = len(search_list) - 1

    while low <= high:
        mid: int = (low + high) // 2
        if search_list[mid] > my_number:
            high = mid - 1
        elif search_list[mid] < my_number:
            low = mid + 1
        else:
            return True
    return False


nu_list = [n for n in range(1_000_000)]
#%%
print("linear, 50000")
%timeit linear_contains(nu_list, 50_000)

# %%
print("binary, 50000")
%timeit binary_contains(nu_list, 50_000)

# %%
print("linear, 723000")
%timeit linear_contains(nu_list, 723_000)

# %%
print("binary, 723000")
%timeit binary_contains(nu_list, 723_000)
# %% 2.
# Add a counter to dfs(), bfs(), and astar() to see how many states each
# searches through for the same maze. Find the counts for 100 different mazes to
# get statistically significant results.
