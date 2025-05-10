#algorithms.py
from collections import deque


def bfs(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    parent = dict()  # To reconstruct the path


    queue = deque([start])
    visited[start[0]][start[1]] = True


    order_visited = []  # For visualization or step counting


    while queue:
        current = queue.popleft()
        order_visited.append(current)


        if current == goal:
            # Reconstruct path after reaching the goal
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()  # Reverse the path to get it from start to goal
            return order_visited, path


        r, c = current  # Get current position
        # Explore neighbors (up, down, left, right)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))


    return order_visited, []
