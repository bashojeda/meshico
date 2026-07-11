from __future__ import annotations

from config import CONFIG
from systems.economy import Economy
from systems.inventory import Inventory
from world.map import MineMap
from world.tile import Tile


class Player:
    PICKAXE_STATS = {
        "wood": 4,
        "iron": 3,
    }
    MINERAL_HARDNESS = {
        "coal": 2,
        "bronze": 2,
        "iron": 4,
        "silver": 4,
        "gold": 4,
        "ruby": 5,
        "emerald": 5,
        "diamond": 6,
    }
    MINERAL_BREAK_CHARS = ("0", "o", "O", "+", "x", "X")

    def __init__(self, x: int, y: int, inventory: Inventory, economy: Economy) -> None:
        self.x = x
        self.y = y
        self.inventory = inventory
        self.economy = economy
        self.health = 3
        self.pickaxe = "wood"
        self.action_message = ""
        self.trader_panel = None
        self.trader_hint = ""

    def move(self, dx: int, dy: int, game_map: MineMap) -> None:
        target_x = self.x + dx
        target_y = self.y + dy
        tile = game_map.get_tile(target_x, target_y)
        if tile.walkable and not (tile.is_mineral and tile.mineral_type):
            self.x = target_x
            self.y = target_y
            self.action_message = ""
            game_map.update_visibility(self.x, self.y, CONFIG.vision_radius)

    def mine(self, dx: int, dy: int, game_map: MineMap) -> None:
        target_x = self.x + dx
        target_y = self.y + dy
        tile = game_map.get_tile(target_x, target_y)
        self.action_message = ""
        if tile.walkable and tile.is_mineral and tile.mineral_type:
            required_hits = self.get_required_hits(tile.mineral_type)
            if self.inventory.get_used_space() >= self.inventory.capacity:
                self.action_message = "Tu mochila está llena"
                return

            tile.mine_hits += 1
            if tile.mine_hits < required_hits:
                stage_index = min(len(self.MINERAL_BREAK_CHARS) - 1, tile.mine_hits - 1)
                tile.char = self.MINERAL_BREAK_CHARS[stage_index]
                self.action_message = f"Rompiendo {tile.mineral_type.title()} ({tile.mine_hits}/{required_hits})"
            else:
                if self.inventory.add_item(tile.mineral_type):
                    game_map.set_tile(target_x, target_y, Tile(char=".", walkable=True))
                    self.action_message = f"Recolectaste {tile.mineral_type.title()}"
                else:
                    self.action_message = "Tu mochila está llena"
        elif tile.char in {"#", "0", "+", "-"}:
            required_hits = self.PICKAXE_STATS.get(self.pickaxe, 4)
            tile.mine_hits += 1
            if tile.mine_hits == 1:
                tile.char = "0"
            elif tile.mine_hits == 2:
                tile.char = "+"
            elif tile.mine_hits == 3 and required_hits >= 4:
                tile.char = "-"
            if tile.mine_hits >= required_hits:
                game_map.set_tile(target_x, target_y, Tile(char=".", walkable=True))
                self.action_message = f"Rompiste la pared con {self.pickaxe}"
            else:
                self.action_message = f"Picando pared ({tile.mine_hits}/{required_hits})"
        else:
            self.action_message = "Nada que picar aquí"

    def get_required_hits(self, mineral_type: str) -> int:
        base_hits = self.MINERAL_HARDNESS.get(mineral_type, 2)
        if self.pickaxe == "iron":
            return max(1, base_hits - 1)
        if self.pickaxe == "gold":
            return max(1, base_hits - 1)
        if self.pickaxe == "diamond":
            return max(1, base_hits - 2)
        return base_hits

    def sell_inventory(self) -> None:
        total = self.inventory.sell_all(self.economy)
        if total > 0:
            self.inventory.clear()
