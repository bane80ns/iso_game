"""
Iso Game - Main loop
"""

import pygame
import sys

from .config import (
    SCREEN_W, SCREEN_H, FPS, TITLE,
    MAP_W, MAP_H, TILE_W, TILE_H, TILE_COLORS,
    WALKABLE, MOVE_SPEED,
    UNEXPLORED, EXPLORED, VISIBLE
)
from .rendering import (
    grid_to_screen, screen_to_grid, world_to_screen,
    draw_diamond, draw_wall, draw_hover, draw_player,
    apply_fog
)
from .game import create_map, create_fow, update_fow, Player
from .pathfinding import find_path


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    font = None

    # Initialization
    game_map = create_map()
    fow = create_fow()
    player = Player(10, 15)

    # Camera - world coordinates
    cam_wx, cam_wy = player.get_world_pos()
    cam_wx, cam_wy = float(cam_wx), float(cam_wy)

    update_fow(fow, player.gx, player.gy)

    hover_gx, hover_gy = -1, -1
    
    running = True
    while running:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()

        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tgx, tgy = screen_to_grid(mx, my, int(cam_wx), int(cam_wy))
                if 0 <= tgx < MAP_W and 0 <= tgy < MAP_H:
                    if WALKABLE.get(game_map[tgy][tgx], False):
                        # If click on last tile of current path, continue/stop
                        if len(player.path) > 0 and player.path[-1] == (tgx, tgy):
                            player.moving = not player.moving
                        else:
                            # Find new path
                            current_path = find_path(player.gx, player.gy, tgx, tgy, game_map)
                            if current_path:
                                player.set_path(current_path)
                            else:
                                # No path, stop
                                player.stop()

        # --- UPDATE ---
        player.update(game_map, MOVE_SPEED)

        # Camera follows player
        pwx, pwy = player.get_world_pos()
        cam_wx += (pwx - cam_wx) * 0.1
        cam_wy += (pwy - cam_wy) * 0.1

        # FoW follows player
        update_fow(fow, player.gx, player.gy)

        # Hover
        hover_gx, hover_gy = screen_to_grid(mx, my, int(cam_wx), int(cam_wy))

        # --- DRAW ---
        screen.fill((10, 10, 20))

        # Draw map
        for y in range(MAP_H):
            for x in range(MAP_W):
                fog = fow[y][x]
                if fog == UNEXPLORED:
                    continue

                tile_type = game_map[y][x]
                base_color = TILE_COLORS.get(tile_type, (80,80,80))
                color = apply_fog(base_color, fog)
                if color is None:
                    continue

                sx, sy = grid_to_screen(x, y, int(cam_wx), int(cam_wy))

                # Frustum cull
                if sx < -TILE_W*2 or sx > SCREEN_W+TILE_W*2:
                    continue
                if sy < -TILE_H*4 or sy > SCREEN_H+TILE_H*2:
                    continue

                is_hover = (x == hover_gx and y == hover_gy and
                           fog == VISIBLE and WALKABLE.get(tile_type, False))

                if tile_type == 3:
                    draw_wall(surface=screen, color=color, sx=sx, sy=sy)
                else:
                    draw_diamond(screen, color, sx, sy)
                    if is_hover:
                        draw_hover(screen, sx, sy)

        # Draw path preview
        for px, py in player.get_path():
            psx, psy = grid_to_screen(px, py, int(cam_wx), int(cam_wy))
            if -TILE_W*2 < psx < SCREEN_W+TILE_W*2 and \
               -TILE_H*4 < psy < SCREEN_H+TILE_H*2:
                draw_hover(screen, psx, psy)

        # Draw player
        psx, psy = world_to_screen(*player.get_world_pos(), int(cam_wx), int(cam_wy))
        draw_player(screen, psx, psy)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
