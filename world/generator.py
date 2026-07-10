import random

from world.map import MineMap
from world.tile import Tile


class MineGenerator:
    def __init__(self, map_instance: MineMap) -> None:
        self.map = map_instance

    def generate(self) -> None:
        mineral_options = [
            ("coal", "C", 0.18),
            ("iron", "I", 0.08),
            ("bronze", "B", 0.04),
            ("silver", "P", 0.025),
            ("gold", "O", 0.015),
            ("diamond", "D", 0.008),
            ("emerald", "E", 0.004),
            ("ruby", "R", 0.0025),
        ]

        def is_wall(x: int, y: int) -> bool:
            if x <= 0 or y <= 0 or x >= self.map.width - 1 or y >= self.map.height - 1:
                return True
            return self.map.get_tile(x, y).char == "#"

        def wall_neighbors(x: int, y: int) -> int:
            count = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    if is_wall(x + dx, y + dy):
                        count += 1
            return count

        for y in range(self.map.height):
            for x in range(self.map.width):
                if x in (0, self.map.width - 1) or y in (0, self.map.height - 1):
                    self.map.set_tile(x, y, Tile(char="#", walkable=False, solid=True))
                else:
                    if random.random() < 0.45:
                        self.map.set_tile(x, y, Tile(char="#", walkable=False, solid=True))
                    else:
                        self.map.set_tile(x, y, Tile(char=".", walkable=True))

        for _ in range(5):
            next_tiles = [[Tile() for _ in range(self.map.width)] for _ in range(self.map.height)]
            for y in range(self.map.height):
                for x in range(self.map.width):
                    if x in (0, self.map.width - 1) or y in (0, self.map.height - 1):
                        next_tiles[y][x] = Tile(char="#", walkable=False, solid=True)
                        continue
                    neighbors = wall_neighbors(x, y)
                    if neighbors >= 5:
                        next_tiles[y][x] = Tile(char="#", walkable=False, solid=True)
                    elif neighbors <= 2:
                        next_tiles[y][x] = Tile(char=".", walkable=True)
                    else:
                        next_tiles[y][x] = Tile(char=self.map.get_tile(x, y).char, walkable=self.map.get_tile(x, y).walkable)
            self.map.tiles = next_tiles

        self._carve_main_path()
        self._place_minerals(mineral_options)
        self.map.set_tile(1, 1, Tile(char="<", walkable=True))
        self.map.set_tile(self.map.width - 2, self.map.height - 2, Tile(char=">", walkable=True))

    def _carve_main_path(self) -> None:
        x, y = 1, 1
        self.map.set_tile(x, y, Tile(char=".", walkable=True))
        target_x = self.map.width - 2
        target_y = self.map.height - 2
        while x != target_x or y != target_y:
            if random.random() < 0.5:
                x += 1 if x < target_x else -1
            else:
                y += 1 if y < target_y else -1
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx = x + dx
                    ny = y + dy
                    if 0 < nx < self.map.width - 1 and 0 < ny < self.map.height - 1:
                        self.map.set_tile(nx, ny, Tile(char=".", walkable=True))

    def _place_minerals(self, mineral_options: list[tuple[str, str, float]]) -> None:
        for y in range(1, self.map.height - 1):
            for x in range(1, self.map.width - 1):
                tile = self.map.get_tile(x, y)
                if not tile.walkable:
                    continue
                if any(isinstance(self.map.get_tile(x + dx, y + dy), Tile) and self.map.get_tile(x + dx, y + dy).char == "#" for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                    if random.random() < 0.25:
                        choice = random.random()
                        current = 0.0
                        for mineral_name, mineral_char, weight in mineral_options:
                            current += weight
                            if choice < current:
                                self.map.set_tile(x, y, Tile(char=mineral_char, walkable=True, is_mineral=True, mineral_type=mineral_name))
                                break
                    else:
                        self.map.set_tile(x, y, Tile(char=".", walkable=True))
                else:
                    self.map.set_tile(x, y, Tile(char=".", walkable=True))
