from collections import deque

def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    rows = len(maze)
    cols = len(maze[0])
    
    start = None
    end = None
    
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
    if not start or not end:
        return {"distance": -1, "path": []}
    conveyor_dirs = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0)
    }

    def process_move(r, c):
        current_r, current_c = r, c
        sub_path = []
        visited_conveyors = set()
        
        while True:
            cell = maze[current_r][current_c]
            if cell in conveyor_dirs:
                if (current_r, current_c) in visited_conveyors:
                    return None
                visited_conveyors.add((current_r, current_c))
                sub_path.append([current_r, current_c])
                dr, dc = conveyor_dirs[cell]
                next_r, next_c = current_r + dr, current_c + dc
                if not (0 <= next_r < rows and 0 <= next_c < cols) or maze[next_r][next_c] == '#':
                    return None
                current_r, current_c = next_r, next_c
            else:
                sub_path.append([current_r, current_c])
                return (current_r, current_c), sub_path
    queue = deque([(start[0], start[1], 0, [[start[0], start[1]]])])
    visited = {(start[0], start[1])}
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c, dist, path = queue.popleft()

        if (r, c) == end:
            return {"distance": dist, "path": path}
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
                result = process_move(nr, nc)
                if result is None:
                    continue  
                (final_r, final_c), sub_path = result
                if (final_r, final_c) not in visited:
                    visited.add((final_r, final_c))
                    new_path = path + sub_path
                    queue.append((final_r, final_c, dist + 1, new_path))
    return {"distance": -1, "path": []}


if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    # Output: {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    # Output: {"distance": -1, "path": []}

    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    # Output: {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}