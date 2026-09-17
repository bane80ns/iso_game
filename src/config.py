"""
Konstante za Iso Game
"""

# EKRAN
SCREEN_W, SCREEN_H = 1280, 720
FPS = 60
TITLE = "Iso Game - Faza 1"

# TILES
TILE_W = 64
TILE_H = 32

# MAPA
MAP_W = 30
MAP_H = 30

# FOG OF WAR
VISION_RADIUS = 6

UNEXPLORED = 0
EXPLORED   = 1
VISIBLE    = 2

# BOJE TILE-OVA
TILE_COLORS = {
    0: (34,  139, 34),    # Trava
    1: (139, 115, 85),    # Zemlja
    2: (30,  144, 255),   # Voda
    3: (100, 100, 100),   # Zid
    4: (0,   80,  0),     # Šuma
}

# PROHODNOST
WALKABLE = {
    0: True,   # Trava
    1: True,   # Zemlja
    2: False,  # Voda
    3: False,  # Zid
    4: True,   # Šuma
}

# KRETANJE
MOVE_SPEED = 4.0
