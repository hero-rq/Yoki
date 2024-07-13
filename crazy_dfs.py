"""
Problem Statement:
Write a Python program to find all connected components in a given undirected graph. 
The graph is represented as an adjacency list, where each node is connected to a list of other nodes. 
Your program should use Depth-First Search (DFS) to identify and list all connected components in the graph. 
A connected component is a set of nodes such that there is a path between any two nodes in this set, 
and no node in the set is connected to any node outside the set.

Your program should output a list of lists, where each inner list contains the nodes of one connected 
component.

Input:
An undirected graph represented as an adjacency list. The graph can be represented as a dictionary 
where the keys are node identifiers and the values are lists of neighboring nodes.

Output:
A list of lists, where each inner list contains the nodes of one connected component.

graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1],
    3: [4],
    4: [3],
    5: []
}

# Output:
# [[0, 1, 2], [3, 4], [5]]
"""


graph = [[0, [1, 2]], [1, [0, 2]], [2, [0, 1]], [3, [4]], [4, [3]], [5, []]]

# Convert the list of lists graph representation to a dictionary
graph_dict = {node[0]: node[1] for node in graph}

def find_cand(graph):
    start = graph[0][0] 
    end = graph[-1][0]  # The end should be the last node, not the last neighbor list
    cand = []
    same = [] 

    def dfs(x):
        for i in range(len(graph)):
            for rx in graph[i][1]:  # Correctly access neighbors
                if rx not in same:  # Check if rx is not in same
                    same.append(rx)
                    cand.append(rx)
                    dfs(graph[rx][1])  # Recursively apply dfs

        return cand

    # Start DFS from the start node
    same.append(start)
    cand.append(start)
    dfs(graph[start][1])

    return cand

result = find_cand(graph)
print("Candidates found:", result)
                    

def dfs(node, graph, visited, component):
    visited.add(node)
    component.append(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, graph, visited, component)

def find_connected_components(graph):
    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            component = []
            dfs(node, graph, visited, component)
            components.append(component)

    return components

graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1],
    3: [4],
    4: [3],
    5: []
}

result = find_connected_components(graph)
print("Connected components:", result)
