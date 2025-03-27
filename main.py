from core.file_reader import read_constraint_table
from core.graph_builder import build_graph, display_matrix
from core.scheduler import (
    detect_cycle_and_compute_ranks,
    compute_earliest_dates,
    compute_latest_dates,
    compute_floats,
    find_critical_paths
)

def main():
    while True:
        filename = input("\nEnter constraint table filename (or 'exit' to quit): ")
        if filename.lower() == 'exit':
            break

        full_path = f"constraints/{filename}"
        tasks = read_constraint_table(full_path)

        if tasks is None:
            continue

        print("\n* Creating the scheduling graph:")
        matrix, nodes = build_graph(tasks)
        print(f"{len(nodes)} vertices")
        edge_count = sum(1 for row in matrix for val in row if isinstance(val, int))
        print(f"{edge_count} edges")
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                if isinstance(matrix[i][j], int):
                    print(f"{chr(65 + nodes[i])} -> {chr(65 + nodes[j])} = {matrix[i][j]}")

        display_matrix(matrix, nodes)

        ranks = detect_cycle_and_compute_ranks(matrix, nodes)
        if ranks is None:
            print("This graph cannot be used as a scheduling graph.")
            continue

        earliest = compute_earliest_dates(matrix, nodes, ranks)
        latest = compute_latest_dates(matrix, nodes, ranks, earliest)
        floats = compute_floats(earliest, latest)
        find_critical_paths(floats)

if __name__ == "__main__":
    main()