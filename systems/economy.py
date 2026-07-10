from __future__ import annotations


class Economy:
    def __init__(self, starting_money: int) -> None:
        self.money = starting_money
        self.prices = {
            "coal": 2,
            "iron": 5,
            "bronze": 8,
            "silver": 12,
            "gold": 20,
            "diamond": 40,
            "emerald": 55,
            "ruby": 75,
        }

    def sell_item(self, item_name: str, quantity: int) -> int:
        price = self.prices.get(item_name, 0)
        total = price * quantity
        self.money += total
        return total
