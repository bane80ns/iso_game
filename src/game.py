"""
Game logic - map, FoW, player state
"""

import math
from .config import (
    MAP_W, MAP_H, VISION_RADIUS,
    UNEXPLORED, EXPLORED, VISIBLE, WALKABLE
)


# ---------------------------------------------------------------------------
# MAP
# ---------------------------------------------------------------------------

def create_map():
    """Generate map."""
    m = []
    for y in range(MAP_H):
        row = []
        for x in range(MAP_W):
            if x == 0 or y == 0 or x == MAP_W-1 or y == MAP_H-1:
                row.append(3)  # Wall
            elif 12 <= x <= 17 and 12 <= y <= 17:
                row.append(2)  # Water
            elif 3 <= x <= 8 and 3 <= y <= 8:
                row.append(4)  # Forest
            elif x == y or x == y+1:
                row.append(1)  # Dirt
            elif (x in (20,25) and 5 <= y <= 9) or \
                 (20 <= x <= 25 and y in (5,9)):
                row.append(3)  # Wall
            else:
                row.append(0)  # Grass
        m.append(row)
    return m


# ---------------------------------------------------------------------------
# FOG OF WAR
# ---------------------------------------------------------------------------

def create_fow():
    """Create FoW matrix."""
    return [[UNEXPLORED]*MAP_W for _ in range(MAP_H)]


def update_fow(fow, player_gx, player_gy):
    """Update FoW based on player position."""
    # Explored tiles remain explored
    for y in range(MAP_H):
        for x in range(MAP_W):
            if fow[y][x] == VISIBLE:
                fow[y][x] = EXPLORED

    # Update visible tiles
    for y in range(MAP_H):
        for x in range(MAP_W):
            if math.sqrt((x-player_gx)**2 + (y-player_gy)**2) <= VISION_RADIUS:
                fow[y][x] = VISIBLE


# ---------------------------------------------------------------------------
# PLAYER
# ---------------------------------------------------------------------------

class Player:
    def __init__(self, gx, gy):
        from .rendering import grid_to_world

        self.gx = gx  # Grid position
        self.gy = gy
        self.wx, self.wy = grid_to_world(gx, gy)  # World smooth position
        self.wx = float(self.wx)
        self.wy = float(self.wy)
        self.path = [(gx, gy)]  # Path to follow
        self.path_index = 0  # Current index in path
        self.moving = False
        self.target_tile = None  # Currently selected target tile
        self.target_reachable = False  # Is target reachable

    def get_grid_pos(self):
        return self.gx, self.gy

    def get_world_pos(self):
        return self.wx, self.wy

    def get_path(self):
        """Return current path."""
        return self.path

    def set_path(self, path):
        """Set new path."""
        if path and len(path) > 1:
            self.path = path
            self.path_index = 0
            self.moving = True
        else:
            self.stop()

    def stop(self):
        """Stop movement."""
        self.moving = False

    def set_target(self, target_gx, target_gy, path):
        """Set target tile and path (if reachable)."""
        self.target_tile = (target_gx, target_gy)
        if path:
            self.path = path
            self.path_index = 0
            self.target_reachable = True
        else:
            self.target_reachable = False
            # Keep current path when target is unreachable

    def start_movement(self):
        """Start moving towards target."""
        if self.target_reachable and self.target_tile:
            self.path_index = 0
            self.moving = True

    def clear_target(self):
        """Clear target and path."""
        self.target_tile = None
        self.target_reachable = False
        self.moving = False
        self.path = [(self.gx, self.gy)]
        self.path_index = 0

    def update(self, game_map, move_speed):
        """Update smooth movement through path."""
        from .rendering import grid_to_world, screen_to_grid, world_to_screen

        if not self.moving or self.path_index >= len(self.path):
            self.moving = False
            return

        # Next tile in path
        next_gx, next_gy = self.path[self.path_index]
        next_wx, next_wy = grid_to_world(next_gx, next_gy)

        dx = next_wx - self.wx
        dy = next_wy - self.wy
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < move_speed:
            # Reached next tile
            self.wx = float(next_wx)
            self.wy = float(next_wy)
            self.gx = next_gx
            self.gy = next_gy
            self.path_index += 1

            if self.path_index >= len(self.path):
                self.moving = False
        else:
            # Move towards next tile
            self.wx += dx / dist * move_speed
            self.wy += dy / dist * move_speed
