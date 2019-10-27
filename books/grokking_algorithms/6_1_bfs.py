#%% bfs
from collections import deque

graph = {
    'ty': ['alicja', 'bartek', 'cecylia'],
    'alicja': ['bartek'],
    'bartek': ['michał', 'igor'],
    'cecylia': ['ty'],
    'michał':  [],
    'igor': []
}


def bfs(graph, src, dest):
    search_queue = deque()
    search_queue += graph[src]
    searched = []

    while search_queue:
        person = search_queue.popleft()
        if person not in searched:
            if person == dest:
                return True
            else:
                search_queue += graph.get(person)
                searched.append(person)
    return False


bfs(graph, 'ty', 'igor')
