from __future__ import annotations

from collections import Counter

from systems.economy import Economy


class Inventory:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.items: Counter[str] = Counter()

    def add_item(self, item_name: str) -> bool:
        if self.get_used_space() >= self.capacity:
            return False
        self.items[item_name] += 1
        return True

    def get_used_space(self) -> int:
        return sum(self.items.values())

    def clear(self) -> None:
        self.items.clear()

    def sell_all(self, economy: Economy) -> int:
        total = 0
        for item_name, quantity in list(self.items.items()):
            total += economy.sell_item(item_name, quantity)
        self.items.clear()
        return total
