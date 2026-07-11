from systems.economy import Economy
from systems.inventory import Inventory
from systems.traders import Trader


def test_celestial_trader_buys_celestial_minerals() -> None:
    inventory = Inventory(capacity=10)
    inventory.add_item("diamond")
    inventory.add_item("emerald")

    economy = Economy(starting_money=0)
    trader = Trader("Celestial Trader", 0, 0, "celestial_buyer")

    result = trader.interact(inventory, economy)

    assert result["sold"] is True
    assert economy.money == 180
    assert inventory.items["diamond"] == 0
    assert inventory.items["emerald"] == 0


def test_bob_sells_pickaxe_when_requirements_are_met() -> None:
    inventory = Inventory(capacity=10)
    inventory.add_item("iron")
    inventory.add_item("coal")

    economy = Economy(starting_money=50)
    trader = Trader("Bob", 0, 0, "pickaxe_seller")

    result = trader.interact(inventory, economy, current_pickaxe="wood")

    assert result["sold"] is True
    assert economy.money == 20
    assert inventory.items["iron"] == 0
    assert inventory.items["coal"] == 0


def test_pointer_direction_for_far_trader() -> None:
    trader = Trader("Bob", 5, 0, "pickaxe_seller")

    assert trader.get_pointer(0, 0) == ">"
