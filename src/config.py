"""
Constants for Iso Game
"""

# SCREEN
SCREEN_W, SCREEN_H = 1280, 720
FPS = 60
TITLE = "Iso Game - Phase 1"

# TILES
TILE_W = 64
TILE_H = 32

# MAP
MAP_W = 30
MAP_H = 30

# FOG OF WAR
VISION_RADIUS = 6

UNEXPLORED = 0
EXPLORED   = 1
VISIBLE    = 2

# TILE COLORS
TILE_COLORS = {
    0: (34,  139, 34),    # Grass
    1: (139, 115, 85),    # Dirt
    2: (30,  144, 255),   # Water
    3: (100, 100, 100),   # Wall
    4: (0,   80,  0),     # Forest
}

# WALKABILITY
WALKABLE = {
    0: True,   # Grass
    1: True,   # Dirt
    2: False,  # Water
    3: False,  # Wall
    4: True,   # Forest
}

# MOVEMENT
MOVE_SPEED = 4.0
