from dataclasses import dataclass


@dataclass
class Tile:
    char: str = "."
    walkable: bool = True
    is_mineral: bool = False
    mineral_type: str | None = None
    solid: bool = False
    revealed: bool = False
    mine_hits: int = 0

    def __str__(self) -> str:
        return self.char
