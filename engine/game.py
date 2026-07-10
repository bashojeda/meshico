import sys

import pygame

from config import CONFIG
from entities.player import Player
from systems.inventory import Inventory
from systems.economy import Economy
from world.generator import MineGenerator
from world.map import MineMap
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

    def update(self) -> None:
        pass

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
                elif tile.revealed:
                    char = tile.char
                else:
                    char = " "
                color = self.get_tile_color(tile)
                text = self.font.render(char, True, color)
                self.screen.blit(text, (10 + col * 8, 10 + row * 14))

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
        if tile.char == "#":
            return (120, 120, 120)
        if tile.char == ".":
            return (50, 50, 50)
        return (0, 255, 0)


if __name__ == "__main__":
    sys.exit(0)
