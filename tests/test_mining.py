from entities.player import Player
from systems.economy import Economy
from systems.inventory import Inventory
from world.map import MineMap
from world.tile import Tile


def test_mineral_breaks_with_hits_and_collects_after_completion() -> None:
    inventory = Inventory(capacity=5)
    economy = Economy(starting_money=0)
    player = Player(x=0, y=0, inventory=inventory, economy=economy)
    game_map = MineMap(width=3, height=3)
    game_map.set_tile(1, 0, Tile(char="C", walkable=True, is_mineral=True, mineral_type="coal"))

    player.mine(1, 0, game_map)
    assert game_map.get_tile(1, 0).char == "0"
    assert game_map.get_tile(1, 0).mine_hits == 1

    player.mine(1, 0, game_map)
    assert inventory.items["coal"] == 1
    assert game_map.get_tile(1, 0).char == "."


def test_diamond_requires_more_hits_than_coal() -> None:
    inventory = Inventory(capacity=5)
    economy = Economy(starting_money=0)
    player = Player(x=0, y=0, inventory=inventory, economy=economy)
    game_map = MineMap(width=3, height=3)
    game_map.set_tile(1, 0, Tile(char="D", walkable=True, is_mineral=True, mineral_type="diamond"))

    for _ in range(5):
        player.mine(1, 0, game_map)

    assert inventory.items["diamond"] == 0
    assert game_map.get_tile(1, 0).mine_hits == 5
    assert game_map.get_tile(1, 0).char == "x"

    player.mine(1, 0, game_map)
    assert inventory.items["diamond"] == 1
