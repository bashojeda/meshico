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

    def __init__(self, x: int, y: int, inventory: Inventory, economy: Economy) -> None:
        self.x = x
        self.y = y
        self.inventory = inventory
        self.economy = economy
        self.health = 3
        self.pickaxe = "wood"
        self.action_message = ""

    def move(self, dx: int, dy: int, game_map: MineMap) -> None:
        target_x = self.x + dx
        target_y = self.y + dy
        tile = game_map.get_tile(target_x, target_y)
        if tile.walkable:
            self.x = target_x
            self.y = target_y
            self.action_message = ""
            game_map.update_visibility(self.x, self.y, CONFIG.vision_radius)
            if tile.is_mineral and tile.mineral_type:
                if self.inventory.add_item(tile.mineral_type):
                    game_map.set_tile(target_x, target_y, Tile(char=".", walkable=True))

    def mine(self, dx: int, dy: int, game_map: MineMap) -> None:
        target_x = self.x + dx
        target_y = self.y + dy
        tile = game_map.get_tile(target_x, target_y)
        self.action_message = ""
        if tile.char in {"#", "0", "+", "-"}:
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
        elif tile.walkable and tile.is_mineral and tile.mineral_type:
            if self.inventory.add_item(tile.mineral_type):
                game_map.set_tile(target_x, target_y, Tile(char=".", walkable=True))
                self.action_message = f"Recolectaste {tile.mineral_type.title()}"
        else:
            self.action_message = "Nada que picar aquí"

    def sell_inventory(self) -> None:
        total = self.inventory.sell_all(self.economy)
        if total > 0:
            self.inventory.clear()
