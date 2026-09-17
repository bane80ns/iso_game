# Iso Game

A 2D isometric tile-based game built with Python and Pygame. Features intelligent pathfinding, fog of war, and smooth camera following.

## Features

- **Isometric Grid System** — 30×30 grid with diamond-shaped tiles
- **A* Pathfinding** — Player navigates around obstacles intelligently
- **Fog of War** — Three states: unexplored (hidden), explored (darkened), visible (fully lit)
- **Smooth Movement** — Fluid animation as player walks along calculated paths
- **Smart Camera** — Follows player without jitter or lag
- **Terrain Variety** — Grass, dirt, water, walls, and forest tiles with distinct walkability

## Installation

### Prerequisites
- Python 3.14+
- Pygame 2.6+

### Setup

```bash
cd /home/bane/Development/iso-game
source venv/bin/activate
python -m src
```

Or directly:
```bash
/home/bane/Development/iso-game/venv/bin/python -m src
```

## How to Play

### Controls
- **Mouse Click** — Select destination tile
  - Click on walkable tile → shows white-framed path preview
  - Click on same tile again → player starts walking
  - Click on unwalkable tile (water/wall) → shows red frame warning
  - Click different tile during preview → recalculates path
  - Click anywhere during movement → stops player at current tile

### Game World
- **Green** — Grass (walkable)
- **Brown** — Dirt (walkable)
- **Blue** — Water (blocked)
- **Gray** — Walls (blocked)
- **Dark Green** — Forest (walkable)

### Vision System
- **Bright tiles** — Currently visible
- **Darkened tiles** — Already explored
- **Black areas** — Unexplored (fog of war)

The player's vision radius is 6 tiles. Explored areas remain visible on the map but darkened when out of direct sight.

## Project Structure

```
src/
├── __main__.py       # Entry point
├── main.py          # Game loop and rendering
├── config.py        # Constants (screen size, tile dimensions, colors)
├── game.py          # Game logic (map generation, FOW, player class)
├── rendering.py     # Coordinate transformations and drawing primitives
└── pathfinding.py   # A* algorithm for path calculation
```

### Key Classes

**Player** — Manages player state, smooth movement, and path following
- `get_world_pos()` — Returns smooth interpolated world coordinates
- `get_grid_pos()` — Returns current grid tile position
- `set_target()` — Sets target tile and calculates path (if reachable)
- `start_movement()` — Begins movement along calculated path
- `update()` — Updates position (called each frame)

**Coordinate Systems**
- **Grid** — Tile position (0-29, 0-29)
- **World** — Continuous isometric coordinates (from grid via `grid_to_world`)
- **Screen** — Pixel coordinates on 1280×720 display (from world via `world_to_screen`)

### Map Generation

Hardcoded in `create_map()`:
- Border walls (tile type 3)
- Central water pool (12-17, 12-17)
- Forest patch (3-8, 3-8)
- Diagonal dirt paths
- Small wall structure

## Current Status

### ✅ Implemented
- A* pathfinding with obstacle avoidance
- Visual path preview (white frames for reachable, red for blocked)
- Fog of war with three visibility states
- Smooth camera tracking
- Player movement along calculated paths
- Terrain walkability system

### 📋 Planned Features
- [ ] Dynamic map generation
- [ ] Multiple NPCs with AI pathfinding
- [ ] Interactive objects (doors, chests, etc.)
- [ ] Combat/interaction system
- [ ] Animated sprites and tile variations
- [ ] Sound effects
- [ ] Save/load system

## Development Notes

- All code is in English (function names, comments, variables)
- User communication is in Serbian
- Pygame coordinate system: origin at top-left, Y increases downward
- Isometric projection: X increases to bottom-right, Y to bottom-left when viewed
- Camera follows player without lerping to avoid jitter

## License

Open source, for learning purposes.
