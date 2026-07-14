from __future__ import annotations

from collections import Counter

from systems.economy import Economy
from systems.inventory import Inventory
from ui.localization import t


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

    def interact(
        self,
        inventory: Inventory,
        economy: Economy,
        current_pickaxe: str | None = None,
        action: str | None = None,
        language: str = "en",
    ) -> dict[str, object]:
        if self.trader_type == "celestial_buyer":
            return self._buy_celestial_minerals(inventory, economy, action, language)
        if self.trader_type == "pickaxe_seller":
            return self._sell_pickaxe(inventory, economy, current_pickaxe, action, language)
        return {"sold": False, "message": t("nothing_to_offer", language)}

    def _buy_celestial_minerals(
        self,
        inventory: Inventory,
        economy: Economy,
        action: str | None,
        language: str,
    ) -> dict[str, object]:
        prices = {"diamond": 80, "emerald": 100, "ruby": 120}
        if action == "prices":
            msg = (
                f"{self.name}: {t('price_list_title', language)}\n"
                f"  {t('mineral_diamond', language)} ${prices['diamond']}\n"
                f"  {t('mineral_emerald', language)} ${prices['emerald']}\n"
                f"  {t('mineral_ruby', language)} ${prices['ruby']}"
            )
            return {"sold": False, "message": msg}
        if action == "sell_coal":
            if inventory.items.get("coal", 0) <= 0:
                return {"sold": False, "message": t("no_coal_to_sell", language, name=self.name)}
            inventory.items["coal"] -= 1
            if inventory.items["coal"] <= 0:
                inventory.items["coal"] = 0
            economy.money += 3
            return {"sold": True, "message": t("paid_for_coal", language, name=self.name, amount=3), "sold_item": "coal"}

        total = 0
        for item_name in ("diamond", "emerald", "ruby"):
            quantity = inventory.items.get(item_name, 0)
            if quantity:
                total += prices[item_name] * quantity
                inventory.items[item_name] = 0

        if total > 0:
            economy.money += total
            return {
                "sold": True,
                "message": t(
                    "paid_for_celestial_minerals",
                    language,
                    name=self.name,
                    total=total,
                ),
                "total": total,
            }
        return {
            "sold": False,
            "message": t("no_celestial_minerals", language, name=self.name),
        }

    def _sell_pickaxe(
        self,
        inventory: Inventory,
        economy: Economy,
        current_pickaxe: str | None,
        action: str | None,
        language: str,
    ) -> dict[str, object]:
        if action == "info":
            return {
                "sold": False,
                "message": t(
                    "need_coal_iron_labor",
                    language,
                    name=self.name,
                ),
            }
        if current_pickaxe == "iron":
            return {
                "sold": False,
                "message": t(
                    "already_best_pickaxe",
                    language,
                    name=self.name,
                ),
            }

        requirements = {"coal": 1, "iron": 1}
        labor_cost = 30
        missing = [
            t(f"mineral_{name}", language) for name, needed in requirements.items()
            if inventory.items.get(name, 0) < needed
        ]
        if missing:
            return {
                "sold": False,
                "message": t(
                    "need_items_for_pickaxe",
                    language,
                    name=self.name,
                    missing=", ".join(missing),
                ),
            }
        if economy.money < labor_cost:
            return {
                "sold": False,
                "message": t(
                    "owe_labor",
                    language,
                    name=self.name,
                    labor_cost=labor_cost,
                ),
            }

        for item_name, required in requirements.items():
            inventory.items[item_name] -= required
            if inventory.items[item_name] <= 0:
                inventory.items[item_name] = 0

        economy.money -= labor_cost
        return {
            "sold": True,
            "message": t(
                "sold_iron_pickaxe",
                language,
                name=self.name,
                labor_cost=labor_cost,
            ),
            "pickaxe": "iron",
        }

    def get_pointer(self, player_x: int, player_y: int) -> str:
        dx = self.x - player_x
        dy = self.y - player_y
        if abs(dx) > abs(dy):
            return ">" if dx > 0 else "<"
        if dy > 0:
            return "v"
        return "^"
