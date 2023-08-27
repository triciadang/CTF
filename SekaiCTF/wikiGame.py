from collections import defaultdict

class Graph:
    def __init__(self, n):
        self.graph = defaultdict(list)
        self.n = n

    def add_edge(self, u, v):
        self.graph[u].append(v)

def build_graph_from_file(file):
    n, m = map(int, file.readline().split())
    graph = Graph(n)

    for _ in range(m):
        u, v = map(int, file.readline().split())
        graph.add_edge(u, v)

    src, dst = map(int, file.readline().split())

    return graph, src, dst


def dfs(graph, start, end, visited, depth, max_depth):
    if start == end:
        return True
    if depth > max_depth:
        return False
    visited[start] = True
    for neighbor in graph.graph[start]:
        if not visited[neighbor]:
            if dfs(graph, neighbor, end, visited, depth + 1, max_depth):
                return True
    return False


def bfs(graph, start, end, max_depth):
    visited = [False] * graph.n
    queue = [(start, 0)]
    visited[start] = True

    while queue:
        current, depth = queue.pop(0)
        if current == end:
            return True
        if depth < max_depth:
            for neighbor in graph.graph[current]:
                if not visited[neighbor]:
                    queue.append((neighbor, depth + 1))
                    visited[neighbor] = True

    return False


# Example usage
filename = '1.in'

with open(filename, 'r') as file:
    T = int(file.readline())


    answer = ""
    for _ in range(T):
        graph, src, dst = build_graph_from_file(file)
        max_path_length = 6


        if bfs(graph, src, dst, max_path_length):
        #if dfs(graph, src, dst, [False] * graph.n, 0, max_path_length):
            answer+="YES\n"
        else:
            answer+="NO\n"

print(answer)
