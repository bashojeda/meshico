import sys

import pygame

from config import CONFIG
from entities.player import Player
from systems.inventory import Inventory
from systems.economy import Economy
from systems.traders import Trader
from world.generator import MineGenerator
from world.map import MineMap
from world.tile import Tile
from ui.hud import HUD


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("ASCII Mines")
        self.screen = pygame.display.set_mode((1000, 700))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("consolas", 16)
        self.view_width = 100
        self.view_height = 40
        self.camera_offset_x = 10

        self.inventory = Inventory(capacity=CONFIG.initial_backpack_capacity)
        self.economy = Economy(starting_money=CONFIG.starting_money)
        self.map = MineMap(width=120, height=80)
        self.generator = MineGenerator(self.map)
        self.generator.generate()
        self.player = Player(x=1, y=1, inventory=self.inventory, economy=self.economy)
        self.traders = [
            Trader("Celestial Trader", 15, 10, "celestial_buyer"),
            Trader("Bob", 30, 15, "pickaxe_seller"),
        ]
        self._place_traders()
        self.map.update_visibility(self.player.x, self.player.y, CONFIG.vision_radius)
        self.hud = HUD(self.font, self.player)

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(CONFIG.fps)

    def handle_events(self) -> None:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
                elif event.key == pygame.K_UP:
                    if keys[pygame.K_SPACE]:
                        self.player.mine(0, -1, self.map)
                    else:
                        self.player.move(0, -1, self.map)
                elif event.key == pygame.K_DOWN:
                    if keys[pygame.K_SPACE]:
                        self.player.mine(0, 1, self.map)
                    else:
                        self.player.move(0, 1, self.map)
                elif event.key == pygame.K_LEFT:
                    if keys[pygame.K_SPACE]:
                        self.player.mine(-1, 0, self.map)
                    else:
                        self.player.move(-1, 0, self.map)
                elif event.key == pygame.K_RIGHT:
                    if keys[pygame.K_SPACE]:
                        self.player.mine(1, 0, self.map)
                    else:
                        self.player.move(1, 0, self.map)
                elif event.key == pygame.K_SPACE:
                    if keys[pygame.K_UP]:
                        self.player.mine(0, -1, self.map)
                    elif keys[pygame.K_DOWN]:
                        self.player.mine(0, 1, self.map)
                    elif keys[pygame.K_LEFT]:
                        self.player.mine(-1, 0, self.map)
                    elif keys[pygame.K_RIGHT]:
                        self.player.mine(1, 0, self.map)
                elif event.key == pygame.K_s:
                    self.player.sell_inventory()
                elif event.key == pygame.K_e:
                    self.interact_with_nearby_trader()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    self.handle_trader_selection(event.key)

    def update(self) -> None:
        # advance trader idle animations
        for trader in self.traders:
            if hasattr(trader, "face_frames") and trader.face_frames:
                trader.idle_index = (trader.idle_index + 1) % len(trader.face_frames)
        # update any open panel frame index
        active = self._find_active_trader()
        if self.player.trader_panel and active:
            self.player.trader_panel["frame_index"] = active.idle_index
        # update hint for approaching trader
        self.update_trader_hint()

        # close panel if player moved away from active trader
        self.update_trader_panel_state()

    def render(self) -> None:
        self.screen.fill((0, 0, 0))
        self.render_ascii_world()
        self.hud.draw(self.screen)
        pygame.display.flip()

    def render_ascii_world(self) -> None:
        half_width = self.view_width // 2
        half_height = self.view_height // 2
        for row in range(self.view_height):
            for col in range(self.view_width):
                map_x = self.player.x - half_width + col - self.camera_offset_x
                map_y = self.player.y - half_height + row
                tile = self.map.get_tile(map_x, map_y)
                if (map_x, map_y) == (self.player.x, self.player.y):
                    char = "@"
                else:
                    trader = self.get_trader_at(map_x, map_y)
                    if trader is not None and tile.revealed:
                        char = trader.symbol
                    elif tile.revealed:
                        char = tile.char
                    else:
                        char = " "
                color = self.get_tile_color(tile)
                if self.get_trader_at(map_x, map_y) is not None:
                    color = (255, 255, 255)
                text = self.font.render(char, True, color)
                self.screen.blit(text, (10 + col * 8, 10 + row * 14))

    def _place_traders(self) -> None:
        for trader in self.traders:
            # mark surrounding shop area as walkable shop tiles using '%'
            for shop_x, shop_y in self._get_trader_shop_tiles(trader.x, trader.y):
                self.map.set_tile(shop_x, shop_y, Tile(char="%", walkable=True, solid=False))
            # trader tile is visible and walkable
            self.map.set_tile(trader.x, trader.y, Tile(char=trader.symbol, walkable=True, solid=False))

    def _get_trader_shop_tiles(self, x: int, y: int) -> list[tuple[int, int]]:
        return [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        ]

    def get_trader_at(self, x: int, y: int) -> Trader | None:
        for trader in self.traders:
            if trader.x == x and trader.y == y:
                return trader
        return None

    def interact_with_nearby_trader(self) -> None:
        for trader in self.traders:
            if abs(trader.x - self.player.x) <= 1 and abs(trader.y - self.player.y) <= 1:
                self.player.trader_panel = self.get_trader_panel(trader)
                # set initial frame index from trader
                self.player.trader_panel["frame_index"] = trader.idle_index
                self.player.trader_panel["message"] = f"Elige una acción"
                self.player.trader_hint = ""
                self.player.action_message = ""
                return
        self.player.action_message = ""
        self.player.trader_panel = None

    def update_trader_panel_state(self) -> None:
        # If a trader panel is open but player is no longer adjacent, close it
        if not self.player.trader_panel:
            return
        active = self._find_active_trader()
        if active is None:
            self.player.trader_panel = None
            self.player.trader_hint = ""

    def handle_trader_selection(self, key: int) -> None:
        if not self.player.trader_panel:
            return
        trader = self._find_active_trader()
        if trader is None:
            return
        option_index = key - pygame.K_1
        if trader.trader_type == "pickaxe_seller":
            action = "info" if option_index == 0 else None
            result = trader.interact(self.player.inventory, self.player.economy, self.player.pickaxe, action)
        else:
            action = "sell_coal" if option_index == 0 else None
            result = trader.interact(self.player.inventory, self.player.economy, self.player.pickaxe, action)
        self.player.trader_panel["message"] = result["message"]
        if result.get("sold") and result.get("pickaxe"):
            self.player.pickaxe = result["pickaxe"]

    def _find_active_trader(self) -> Trader | None:
        for trader in self.traders:
            if abs(trader.x - self.player.x) <= 1 and abs(trader.y - self.player.y) <= 1:
                return trader
        return None

    def get_trader_panel(self, trader: Trader) -> dict[str, object]:
        if trader.trader_type == "pickaxe_seller":
            return {
                "name": trader.name,
                "face": [
                    "   /~\\   ",
                    "  ( o )  ",
                    "  /  ~\\  ",
                    "  /__|__\\ ",
                ],
                "options": ["Comprar pico de hierro", "Ver requisitos"],
                "details": ["Requisitos: 1 carbón, 1 hierro", "Costo: $30 de mano de obra"],
                "message": "Bob te espera",
            }
        return {
            "name": trader.name,
            "face": [
                "   .-^^-.  ",
                "  ( o  o ) ",
                "   \\  Y  /  ",
                "    `--'   ",
            ],
            "options": ["Vender carbón"],
            "details": ["Precios: diamante $80", "esmeralda $100", "rubí $120"],
            "message": "Celestial te escucha",
        }

    def update_trader_hint(self) -> None:
        trader = self._find_active_trader()
        if trader is not None and not self.player.trader_panel:
            self.player.trader_hint = f"E para interactuar con {trader.name}"
        else:
            self.player.trader_hint = ""

    def get_tile_color(self, tile) -> tuple[int, int, int]:
        colors = {
            "coal": (100, 100, 100),
            "iron": (180, 180, 180),
            "bronze": (205, 127, 50),
            "silver": (192, 192, 192),
            "gold": (255, 215, 0),
            "diamond": (180, 230, 255),
            "emerald": (0, 180, 90),
            "ruby": (220, 20, 60),
        }
        if tile.is_mineral and tile.mineral_type:
            return colors.get(tile.mineral_type, (0, 255, 0))
        if tile.char in {"0", "o", "O", "+", "x", "X"}:
            return (255, 255, 255)
        if tile.char == "#":
            return (120, 120, 120)
        if tile.char == ".":
            return (50, 50, 50)
        return (0, 255, 0)


if __name__ == "__main__":
    sys.exit(0)
