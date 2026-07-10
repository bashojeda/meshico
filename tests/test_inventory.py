from systems.inventory import Inventory
from systems.economy import Economy


def test_inventory_capacity_and_sale() -> None:
    inventory = Inventory(capacity=2)
    assert inventory.add_item("coal") is True
    assert inventory.add_item("iron") is True
    assert inventory.add_item("gold") is False

    economy = Economy(starting_money=0)
    total = inventory.sell_all(economy)

    assert total == 7
    assert economy.money == 7
    assert inventory.get_used_space() == 0
