#%%
from datetime import time, timedelta, datetime

a_meetings = [
    (time(hour=9, minute=0), time(hour=10, minute=30)),
    (time(hour=12, minute=0), time(hour=13, minute=0)),
    (time(hour=16, minute=0), time(hour=18, minute=0)),
]
a_day = [time(hour=9, minute=0), time(hour=20, minute=0)]

b_meetings = [
    (time(hour=10, minute=0), time(hour=11, minute=30)),
    (time(hour=12, minute=30), time(hour=14, minute=30)),
    (time(hour=16, minute=0), time(hour=17, minute=0)),
]
b_day = [time(hour=10, minute=0), time(hour=18, minute=30)]

meeting_duration = 30

# a_meets = [(a_day[0], a_day[0])] + a_meetings + [(a_day[1], a_day[1])]

# a_meets
# for i in range(len(a_meets) - 1):
#     free_time = a_meets[i + 1][0] - a_meets[i][1]


def get_freetime(meetings, day_range, meeting_time):
    flatten = [day_range[0]]
    for a in a_meetings:
        for b in a:
            flatten.append(b)
    flatten.append(day_range[1])

    free_time = []
    for i in range(len(flatten) - 1):
        ft = (flatten[i + 1], flatten[i])
        if ft[1].minutes - ft[0].minutes >= meeting_time:
            free_time.append(ft)

    return flatten


a = get_freetime(a_meetings, a_day, meeting_duration)
b = get_freetime(b_meetings, b_day, meeting_duration)

a
# %%
a_meetings[0][1] - a_meetings[0][0]

# %%
gr = a_meetings[0][1]

gr - gr

# %%
