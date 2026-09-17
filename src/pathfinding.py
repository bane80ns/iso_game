"""
Pathfinding - A* algorithm
"""

import heapq

def find_path(start_x, start_y, end_x, end_y, game_map):
    """
    Find path from start to end using A*.
    Returns list of (gx, gy) coordinates, or None if no path exists.
    """
    from .config import MAP_W, MAP_H, WALKABLE

    def heuristic(x, y):
        return abs(x - end_x) + abs(y - end_y)

    open_set = [(0, start_x, start_y)]
    came_from = {}
    g_score = {(start_x, start_y): 0}
    closed_set = set()

    while open_set:
        _, x, y = heapq.heappop(open_set)

        if (x, y) in closed_set:
            continue

        if x == end_x and y == end_y:
            path = [(x, y)]
            while (x, y) in came_from:
                x, y = came_from[(x, y)]
                path.append((x, y))
            return list(reversed(path))

        closed_set.add((x, y))

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < MAP_W and 0 <= ny < MAP_H):
                continue
            if not WALKABLE.get(game_map[ny][nx], False):
                continue
            if (nx, ny) in closed_set:
                continue

            tentative_g = g_score[(x, y)] + 1

            if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                came_from[(nx, ny)] = (x, y)
                g_score[(nx, ny)] = tentative_g
                f = tentative_g + heuristic(nx, ny)
                heapq.heappush(open_set, (f, nx, ny))

    return None
