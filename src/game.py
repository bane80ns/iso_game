"""
Igra logika - mapa, FoW, stanje igrača
"""

import math
from .config import (
    MAP_W, MAP_H, VISION_RADIUS,
    UNEXPLORED, EXPLORED, VISIBLE, WALKABLE
)


# ---------------------------------------------------------------------------
# MAPA
# ---------------------------------------------------------------------------

def create_map():
    """Generiši mapu."""
    m = []
    for y in range(MAP_H):
        row = []
        for x in range(MAP_W):
            if x == 0 or y == 0 or x == MAP_W-1 or y == MAP_H-1:
                row.append(3)  # Zid
            elif 12 <= x <= 17 and 12 <= y <= 17:
                row.append(2)  # Voda
            elif 3 <= x <= 8 and 3 <= y <= 8:
                row.append(4)  # Šuma
            elif x == y or x == y+1:
                row.append(1)  # Zemlja
            elif (x in (20,25) and 5 <= y <= 9) or \
                 (20 <= x <= 25 and y in (5,9)):
                row.append(3)  # Zid
            else:
                row.append(0)  # Trava
        m.append(row)
    return m


# ---------------------------------------------------------------------------
# FOG OF WAR
# ---------------------------------------------------------------------------

def create_fow():
    """Kreiraj FoW matricu."""
    return [[UNEXPLORED]*MAP_W for _ in range(MAP_H)]


def update_fow(fow, pgx, pgy):
    """Ažuriraj FoW na osnovu pozicije igrača."""
    # Explored ostaju explored
    for y in range(MAP_H):
        for x in range(MAP_W):
            if fow[y][x] == VISIBLE:
                fow[y][x] = EXPLORED
    
    # Ažuriraj vidljive tile-ove
    for y in range(MAP_H):
        for x in range(MAP_W):
            if math.sqrt((x-pgx)**2 + (y-pgy)**2) <= VISION_RADIUS:
                fow[y][x] = VISIBLE


# ---------------------------------------------------------------------------
# IGRAČ
# ---------------------------------------------------------------------------

class Player:
    def __init__(self, gx, gy):
        self.gx = gx  # Grid pozicija
        self.gy = gy
        self.wx = 0.0  # World smooth pozicija
        self.wy = 0.0
        self.target_gx = gx
        self.target_gy = gy
        self.moving = False
    
    def get_grid_pos(self):
        return self.gx, self.gy
    
    def get_world_pos(self):
        return self.wx, self.wy
    
    def set_target(self, tgx, tgy, game_map):
        """Postavi ciljnu poziciju."""
        if 0 <= tgx < MAP_W and 0 <= tgy < MAP_H:
            if WALKABLE.get(game_map[tgy][tgx], False):
                self.target_gx = tgx
                self.target_gy = tgy
                self.moving = True
    
    def update(self, game_map, move_speed):
        """Ažuriraj smooth kretanje igrača."""
        from .rendering import grid_to_world, screen_to_grid, world_to_screen
        
        twx, twy = grid_to_world(self.target_gx, self.target_gy)
        dx = twx - self.wx
        dy = twy - self.wy
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist < move_speed:
            self.wx = float(twx)
            self.wy = float(twy)
            self.gx = self.target_gx
            self.gy = self.target_gy
            self.moving = False
        else:
            self.wx += dx / dist * move_speed
            self.wy += dy / dist * move_speed
            # Ažuriraj grid poziciju na osnovu smooth pozicije
            self.gx, self.gy = screen_to_grid(
                *world_to_screen(self.wx, self.wy, 0, 0), 0, 0
            )
