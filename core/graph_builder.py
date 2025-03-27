def build_graph(tasks):
    task_ids = sorted(tasks.keys())
    n = len(task_ids)
    fictitious_start = 0
    fictitious_end = n + 1
    all_nodes = [fictitious_start] + task_ids + [fictitious_end]

    size = len(all_nodes)
    matrix = [["*" for _ in range(size)] for _ in range(size)]

    index_map = {task: i + 1 for i, task in enumerate(task_ids)}
    index_map[fictitious_start] = 0
    index_map[fictitious_end] = size - 1

    for task, info in tasks.items():
        if not info['predecessors']:
            matrix[0][index_map[task]] = 0
        for pred in info['predecessors']:
            matrix[index_map[pred]][index_map[task]] = tasks[pred]['duration']

    all_preds = set()
    for info in tasks.values():
        all_preds.update(info['predecessors'])
    for task in tasks:
        if task not in all_preds:
            matrix[index_map[task]][size - 1] = tasks[task]['duration']

    return matrix, all_nodes

def display_matrix(matrix, nodes):
    #the first row should be a "a" that we called alpha
    print("\nValue Matrix:")
    
    # Map nodes to letters (A, B, C, ...)
    node_labels = [chr(65 + i - 1) for i in range(len(nodes))]
    node_labels[0] = 'a'  # Start node

    # Display header row with letters
    header = "    " + "  ".join(f"{label:>2}" for label in node_labels)
    print(header)
    
    # Display each row with corresponding letter and matrix values
    for i, row in enumerate(matrix):
        line = f"{node_labels[i]:>2}  " + "  ".join(f"{str(cell):>2}" for cell in row)
        print(line)
