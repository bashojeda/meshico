from world.map import MineMap


def test_viewport_is_centered_on_player() -> None:
    game_map = MineMap(width=11, height=11)
    visible_positions = game_map.get_visible_tiles(center_x=5, center_y=5, radius=2, view_width=5, view_height=5)

    assert (5, 5) in visible_positions
    assert (3, 3) in visible_positions
    assert (7, 7) in visible_positions
    assert (0, 0) not in visible_positions
