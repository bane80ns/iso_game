"""
Rendering i koordinatne transformacije
"""

import pygame
from .config import (
    SCREEN_W, SCREEN_H, TILE_W, TILE_H, 
    UNEXPLORED, EXPLORED, VISIBLE
)


# ---------------------------------------------------------------------------
# KOORDINATNE FUNKCIJE
# ---------------------------------------------------------------------------

def grid_to_world(gx, gy):
    """Grid -> world (izometrijske) koordinate."""
    wx = (gx - gy) * (TILE_W // 2)
    wy = (gx + gy) * (TILE_H // 2)
    return wx, wy


def world_to_screen(wx, wy, cam_wx, cam_wy):
    """World -> screen koordinate."""
    sx = wx - cam_wx + SCREEN_W // 2
    sy = wy - cam_wy + SCREEN_H // 2
    return sx, sy


def grid_to_screen(gx, gy, cam_wx, cam_wy):
    """Grid -> screen direktno."""
    wx, wy = grid_to_world(gx, gy)
    return world_to_screen(wx, wy, cam_wx, cam_wy)


def screen_to_grid(mx, my, cam_wx, cam_wy):
    """Screen -> grid koordinate (inverzna transformacija)."""
    wx = mx - SCREEN_W // 2 + cam_wx
    wy = my - SCREEN_H // 2 + cam_wy
    gx = (wx / (TILE_W // 2) + wy / (TILE_H // 2)) / 2
    gy = (wy / (TILE_H // 2) - wx / (TILE_W // 2)) / 2
    return int(round(gx)), int(round(gy))


# ---------------------------------------------------------------------------
# CRTANJE
# ---------------------------------------------------------------------------

def draw_diamond(surface, color, sx, sy, w=TILE_W, h=TILE_H, border=True):
    """Crta dijamant (tile)."""
    pts = [
        (sx + w // 2, sy),
        (sx + w,      sy + h // 2),
        (sx + w // 2, sy + h),
        (sx,          sy + h // 2),
    ]
    pygame.draw.polygon(surface, color, pts)
    if border:
        dark = tuple(max(0, c - 40) for c in color)
        pygame.draw.polygon(surface, dark, pts, 1)


def draw_wall(surface, color, sx, sy):
    """Crta 3D zid sa senkom."""
    wall_h = TILE_H
    w, h = TILE_W, TILE_H
    top = [
        (sx + w//2, sy - wall_h),
        (sx + w,    sy + h//2 - wall_h),
        (sx + w//2, sy + h - wall_h),
        (sx,        sy + h//2 - wall_h),
    ]
    left = [
        (sx,        sy + h//2 - wall_h),
        (sx + w//2, sy + h - wall_h),
        (sx + w//2, sy + h),
        (sx,        sy + h//2),
    ]
    right = [
        (sx + w//2, sy + h - wall_h),
        (sx + w,    sy + h//2 - wall_h),
        (sx + w,    sy + h//2),
        (sx + w//2, sy + h),
    ]
    dark  = tuple(max(0, c - 50)  for c in color)
    darker = tuple(max(0, c - 90)  for c in color)
    pygame.draw.polygon(surface, color,  top)
    pygame.draw.polygon(surface, dark,   left)
    pygame.draw.polygon(surface, darker, right)
    for pts in [top, left, right]:
        pygame.draw.polygon(surface, (0,0,0), pts, 1)


def draw_hover(surface, sx, sy):
    """Hover highlight za tile."""
    pts = [
        (sx + TILE_W//2, sy),
        (sx + TILE_W,    sy + TILE_H//2),
        (sx + TILE_W//2, sy + TILE_H),
        (sx,             sy + TILE_H//2),
    ]
    s = pygame.Surface((TILE_W, TILE_H), pygame.SRCALPHA)
    local = [(p[0]-sx, p[1]-sy) for p in pts]
    pygame.draw.polygon(s, (255, 255, 255, 60), local)
    surface.blit(s, (sx, sy))
    pygame.draw.polygon(surface, (255, 255, 200), pts, 2)


def draw_player(surface, px, py):
    """Crta igrača na screen koordinatama."""
    cx = px + TILE_W // 2
    cy = py + TILE_H // 2
    # Senka
    pygame.draw.ellipse(surface, (0,0,0), (cx-10, cy-2, 20, 8))
    # Noge
    pygame.draw.rect(surface, (40, 40, 120),  (cx-5, cy-12, 4, 10))
    pygame.draw.rect(surface, (40, 40, 120),  (cx+1, cy-12, 4, 10))
    # Telo
    pygame.draw.rect(surface, (70, 130, 180), (cx-7, cy-26, 14, 14))
    # Glava
    pygame.draw.circle(surface, (255, 220, 177), (cx, cy-32), 7)
    pygame.draw.circle(surface, (0,0,0),          (cx, cy-32), 7, 1)


def apply_fog(color, fog):
    """Primeni FoW filter na boju."""
    if fog == UNEXPLORED:
        return None
    if fog == EXPLORED:
        return tuple(int(c * 0.35) for c in color)
    return color
