from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    screen_width: int = 100
    screen_height: int = 60
    tile_size: int = 1
    fps: int = 20
    initial_backpack_capacity: int = 20
    starting_money: int = 100
    vision_radius: int = 20


CONFIG = GameConfig()
