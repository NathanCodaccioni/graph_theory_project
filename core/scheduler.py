def build_adjacency_list(matrix, nodes):
    from collections import defaultdict
    adj = defaultdict(list)
    n = len(nodes)

    for i in range(n):
        for j in range(n):
            if isinstance(matrix[i][j], int):
                adj[nodes[i]].append(nodes[j])
    return adj

def detect_cycle_and_compute_ranks(matrix, nodes):
    n = len(nodes)
    adj = build_adjacency_list(matrix, nodes)
    in_degree = {node: 0 for node in nodes}

    for u in adj:
        for v in adj[u]:
            in_degree[v] += 1

    from collections import deque
    queue = deque([node for node in nodes if in_degree[node] == 0])
    ranks = {}
    step = 0

    print("\n* Detecting a cycle\n* Method of eliminating entry points")

    while queue:
        print(f"Entry points: {[chr(97) if node == 0 else chr(65 + node - 1) for node in queue]}")
        for _ in range(len(queue)):
            u = queue.popleft()
            ranks[u] = step
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        step += 1

    if len(ranks) != n:
        print("-> There IS a cycle")
        return None
    else:
        print("-> There is NO cycle")
        print("\nRanks of vertices:")
        for node in sorted(ranks):
            label = chr(97) if node == 0 else chr(65 + node - 1)
            print(f"Node {label}: Rank {ranks[node]}")
        return ranks

def compute_earliest_dates(matrix, nodes, ranks):
    earliest = {node: 0 for node in nodes}
    sorted_nodes = sorted(nodes, key=lambda x: ranks[x])
    for u in sorted_nodes:
        for v_idx, cost in enumerate(matrix[nodes.index(u)]):
            if isinstance(cost, int):
                v = nodes[v_idx]
                earliest[v] = max(earliest[v], earliest[u] + cost)
    print("\nEarliest Dates:")
    for node in earliest:
        label = chr(97) if node == 0 else chr(65 + node - 1)
        print(f"Node {label}: {earliest[node]}")
    return earliest

def compute_latest_dates(matrix, nodes, ranks, earliest):
    latest = {node: earliest[nodes[-1]] for node in nodes}
    sorted_nodes = sorted(nodes, key=lambda x: ranks[x], reverse=True)
    for u in sorted_nodes:
        for v_idx, cost in enumerate(matrix[nodes.index(u)]):
            if isinstance(cost, int):
                v = nodes[v_idx]
                latest[u] = min(latest[u], latest[v] - cost)
    print("\nLatest Dates:")
    for node in latest:
        label = chr(97) if node == 0 else chr(65 + node - 1)
        print(f"Node {label}: {latest[node]}")
    return latest

def compute_floats(earliest, latest):
    floats = {}
    print("\nFloat (margin) for each task:")
    for node in earliest:
        label = chr(97) if node == 0 else chr(65 + node - 1)
        floats[node] = latest[node] - earliest[node]
        print(f"Node {label}: {floats[node]}")
    return floats

def find_critical_paths(floats):
    print("\nCritical Path:")
    critical_nodes = [node for node, fl in floats.items() if fl == 0]
    critical_path_labels = [chr(97) if node == 0 else chr(65 + node - 1) for node in critical_nodes]
    print(" -> ".join(critical_path_labels))
    return critical_nodes
