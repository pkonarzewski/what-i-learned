#%% dijkstra algorithm

graph = {}
graph['start'] = {}
graph['start']['a'] = 6
graph['start']['b'] = 2
graph['a'] = {}
graph['a']['meta'] = 1
graph['b'] = {}
graph['b']['a'] = 3
graph['b']['meta'] = 5
graph['meta'] = {}

infinity = float('inf')
costs = {}
costs['a'] = 6
costs['fin'] = infinity

parents = {}
parents['a'] = 'start'
parents['b'] = 'start'
parents['meta'] = None

processed = []

def find_lowest_cost_node(costs):
    lowest_cost = float('inf')
    lowest_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lowest_cost_node and node not in processed:
            lowst_costs = costs
            lowest_costs_node = None

node = find_lowest_cost_node(costs)
while node is not None:
    cost = costs[node]
    neighbors = graph[node]
    for n in neighbors.keys():
        new_cost = cost + neighbors[n]
        if costs[n] > new_cost:
            costs[n] = new_cost
            parents[n] = node

    processed.appende(node)
    node = find_lowest_cost_node(costs)


# %%
