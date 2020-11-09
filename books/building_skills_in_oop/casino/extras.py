#%%
from collections import defaultdict

def create_dice_frequency():
    freq = defaultdict(int)
    for d1 in range(1, 7):
        for d2 in range(1, 7):
            freq[d1+d2] += 1


    for n in range(2, 13):
        print(f"{n:02d}: {'*' * freq[n]}")

create_dice_frequency()
# %%
