from __future__ import annotations

from collections import Counter

from systems.economy import Economy
from systems.inventory import Inventory


class Trader:
    def __init__(self, name: str, x: int, y: int, trader_type: str) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.trader_type = trader_type
        self.symbol = "C" if trader_type == "celestial_buyer" else "B"
        # idle animation frames (simple two-frame subtle animation)
        if trader_type == "celestial_buyer":
            self.face_frames = [
                [
                    "   .-^^-.  ",
                    "  ( o  o ) ",
                    "   \\  Y  / ",
                    "    `--'   ",
                ],
                [
                    "   .-^^-.  ",
                    "  ( -  - ) ",
                    "   \\  Y  / ",
                    "    `--'   ",
                ],
            ]
        else:
            # Bob: bearded man (two-frame blink/movement)
            self.face_frames = [
                [
                    "   _____  ",
                    "  / 0 0 \\ ",
                    " |  \\_/  | ",
                    " |  \\_/  | ",
                    "  \\_____/  ",
                ],
                [
                    "   _____  ",
                    "  / - - \\ ",
                    " |  \\_/  | ",
                    " |  \\_/  | ",
                    "  \\_____/  ",
                ],
            ]
        self.idle_index = 0

    def interact(self, inventory: Inventory, economy: Economy, current_pickaxe: str | None = None, action: str | None = None) -> dict[str, object]:
        if self.trader_type == "celestial_buyer":
            return self._buy_celestial_minerals(inventory, economy, action)
        if self.trader_type == "pickaxe_seller":
            return self._sell_pickaxe(inventory, economy, current_pickaxe, action)
        return {"sold": False, "message": "No tengo nada que ofrecerte."}

    def _buy_celestial_minerals(self, inventory: Inventory, economy: Economy, action: str | None) -> dict[str, object]:
        prices = {"diamond": 80, "emerald": 100, "ruby": 120}
        if action == "prices":
            msg = (
                f"{self.name}: precios ->\n"
                f"  diamante ${prices['diamond']}\n"
                f"  esmeralda ${prices['emerald']}\n"
                f"  rubí ${prices['ruby']}"
            )
            return {"sold": False, "message": msg}
        if action == "sell_coal":
            if inventory.items.get("coal", 0) <= 0:
                return {"sold": False, "message": f"{self.name}:\nno tienes carbón para vender."}
            inventory.items["coal"] -= 1
            if inventory.items["coal"] <= 0:
                inventory.items["coal"] = 0
            economy.money += 3
            return {"sold": True, "message": f"{self.name}:\nte pagué $3 por 1 carbón.", "sold_item": "coal"}

        total = 0
        for item_name in ("diamond", "emerald", "ruby"):
            quantity = inventory.items.get(item_name, 0)
            if quantity:
                total += prices[item_name] * quantity
                inventory.items[item_name] = 0

        if total > 0:
            economy.money += total
            return {"sold": True, "message": f"{self.name}:\nte pagué ${total} por tus minerales celestiales.", "total": total}
        return {"sold": False, "message": f"{self.name}: no tienes minerales celestiales para vender."}

    def _sell_pickaxe(self, inventory: Inventory, economy: Economy, current_pickaxe: str | None, action: str | None) -> dict[str, object]:
        if action == "info":
            return {"sold": False, "message": f"{self.name}: necesito 1 carbón, 1 hierro y $30 de mano de obra para venderte un pico de hierro."}
        if current_pickaxe == "iron":
            return {"sold": False, "message": f"{self.name}: ya tienes el pico más fuerte."}

        requirements = {"coal": 1, "iron": 1}
        labor_cost = 30
        missing = [name for name, needed in requirements.items() if inventory.items.get(name, 0) < needed]
        if missing:
            return {"sold": False, "message": f"{self.name}: necesitas {', '.join(missing)} para ese pico."}
        if economy.money < labor_cost:
            return {"sold": False, "message": f"{self.name}: me debes ${labor_cost} por la mano de obra."}

        for item_name, required in requirements.items():
            inventory.items[item_name] -= required
            if inventory.items[item_name] <= 0:
                inventory.items[item_name] = 0

        economy.money -= labor_cost
        return {"sold": True, "message": f"{self.name}: te vendí un pico de hierro por ${labor_cost} de mano de obra.", "pickaxe": "iron"}

    def get_pointer(self, player_x: int, player_y: int) -> str:
        dx = self.x - player_x
        dy = self.y - player_y
        if abs(dx) > abs(dy):
            return ">" if dx > 0 else "<"
        if dy > 0:
            return "v"
        return "^"
