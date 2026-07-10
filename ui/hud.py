import pygame


class HUD:
    def __init__(self, font: pygame.font.Font, player) -> None:
        self.font = font
        self.player = player

    def draw(self, screen: pygame.Surface) -> None:
        lines = [
            "ASCII Mines",
            f"Money: ${self.player.economy.money}",
            f"Health: {self.player.health}",
            f"Pickaxe: {self.player.pickaxe.title()}",
            f"Action: {self.player.action_message}",
            f"Backpack: {self.player.inventory.get_used_space()}/{self.player.inventory.capacity} | Coal: {self.player.inventory.items.get('coal', 0)} | Iron: {self.player.inventory.items.get('iron', 0)} | Bronze: {self.player.inventory.items.get('bronze', 0)} | Silver: {self.player.inventory.items.get('silver', 0)} | Gold: {self.player.inventory.items.get('gold', 0)} | Diamond: {self.player.inventory.items.get('diamond', 0)} |Emerald: {self.player.inventory.items.get('emerald', 0)} | Ruby: {self.player.inventory.items.get('ruby', 0)}",
            "Controls:",
            "Hold arrow + Space = mine wall | Move = arrows | S = sell | Q/Esc = quit",
        ]
        for index, line in enumerate(lines):
            text = self.font.render(line, True, (0, 255, 0))
            screen.blit(text, (10, 480 + index * 16))
