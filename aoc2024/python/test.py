f = open("input/day02", "r")
count = 0

for i in f:
    j = list(map(int, i.split()))
    if j[0] > j[1]:
        m = -1
    elif j[0] < j[1]:
        m = 1
    else:
        m = 0

    t = False
    for x in range(len(j) - 1):
        if 0 < (j[x + 1] - j[x]) * m < 4:
            t = True
        else:
            t = False
            break
    if not t and x == len(j) - 2:
        t = True
    if not t:
        k = j.copy()
        del k[x]
        if k[0] > k[1]:
            m = -1
        elif k[0] < k[1]:
            m = 1
        else:
            m = 0

        for y in range(len(k) - 1):
            if 0 < (k[y + 1] - k[y]) * m < 4:
                t = True
            else:
                t = False
                break
    if not t:
        k = j.copy()
        del k[x + 1]

        if k[0] > k[1]:
            m = -1
        elif k[0] < k[1]:
            m = 1
        else:
            m = 0

        for y in range(len(k) - 1):
            if 0 < (k[y + 1] - k[y]) * m < 4:
                t = True
            else:
                t = False
                break
    if not t and x != 0:
        k = j.copy()
        del k[x - 1]

        if k[0] > k[1]:
            m = -1
        elif k[0] < k[1]:
            m = 1
        else:
            m = 0

        for y in range(len(k) - 1):
            if 0 < (k[y + 1] - k[y]) * m < 4:
                t = True
            else:
                t = False
                break
    if t:
        count += 1

print(count)
