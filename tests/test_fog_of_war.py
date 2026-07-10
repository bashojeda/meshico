from world.map import MineMap
from world.tile import Tile


def test_reveal_area_marks_tiles_within_radius() -> None:
    game_map = MineMap(width=7, height=7)
    game_map.set_tile(3, 3, Tile(char=".", walkable=True))
    game_map.set_tile(4, 3, Tile(char="C", walkable=True, is_mineral=True, mineral_type="coal"))

    game_map.update_visibility(3, 3, 2)

    assert game_map.get_tile(3, 3).revealed is True
    assert game_map.get_tile(4, 3).revealed is True
    assert game_map.get_tile(0, 0).revealed is False
