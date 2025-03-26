def read_constraint_table(filepath):
    tasks = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = list(map(int, line.strip().split()))
                if len(parts) >= 2:
                    task_id = parts[0]
                    duration = parts[1]
                    predecessors = parts[2:] if len(parts) > 2 else []
                    tasks[task_id] = {
                        'duration': duration,
                        'predecessors': predecessors
                    }
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        return None
    except ValueError:
        print(f"[ERROR] Malformed line in file: {line}")
        return None

    return tasks
