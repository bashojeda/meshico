from __future__ import annotations

from world.tile import Tile


class MineMap:
    def __init__(self, width: int = 80, height: int = 40) -> None:
        self.width = width
        self.height = height
        self.tiles: list[list[Tile]] = [[Tile() for _ in range(width)] for _ in range(height)]

    def get_tile(self, x: int, y: int) -> Tile:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return Tile(char="#", walkable=False, solid=True)

    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile

    def update_visibility(self, x: int, y: int, radius: int) -> None:
        for row in self.tiles:
            for tile in row:
                tile.revealed = False

        aspect = 14 / 8
        for tile_y in range(max(0, y - radius), min(self.height, y + radius + 1)):
            for tile_x in range(max(0, x - radius), min(self.width, x + radius + 1)):
                dx = tile_x - x
                dy = tile_y - y
                if dx * dx + (dy * aspect) * (dy * aspect) <= radius * radius:
                    self.tiles[tile_y][tile_x].revealed = True

    def is_revealed(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x].revealed
        return False

    def get_visible_tiles(self, center_x: int, center_y: int, radius: int, view_width: int, view_height: int) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        half_width = view_width // 2
        half_height = view_height // 2
        for tile_y in range(center_y - half_height, center_y + half_height + 1):
            for tile_x in range(center_x - half_width, center_x + half_width + 1):
                if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
                    positions.append((tile_x, tile_y))
        return positions
