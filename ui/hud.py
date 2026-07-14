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
            f"Hint: {self.player.trader_hint}",
            f"Backpack: {self.player.inventory.get_used_space()}/{self.player.inventory.capacity} | Coal: {self.player.inventory.items.get('coal', 0)} | Iron: {self.player.inventory.items.get('iron', 0)} | Bronze: {self.player.inventory.items.get('bronze', 0)}",
            f"Silver: {self.player.inventory.items.get('silver', 0)} | Gold: {self.player.inventory.items.get('gold', 0)} | Diamond: {self.player.inventory.items.get('diamond', 0)} | Emerald: {self.player.inventory.items.get('emerald', 0)} | Ruby: {self.player.inventory.items.get('ruby', 0)}",
            "Controls:",
            "Hold arrow + Space = mine wall | Move = arrows | S = sell | E = interact | Q/Esc = quit",
        ]
        for index, line in enumerate(lines):
            text = self.font.render(line, True, (0, 255, 0))
            screen.blit(text, (10, 480 + index * 16))

        trader_panel = getattr(self.player, "trader_panel", None)
        if trader_panel:
            self._draw_trader_panel(screen, trader_panel)

    def _draw_trader_panel(self, screen: pygame.Surface, trader_panel: dict[str, object]) -> None:
        x = 700
        y = 180
        # support animated face frames
        frames = trader_panel.get("face_frames") or [trader_panel.get("face", ["  o   o  ", "  |___|  ", "  /|_|\\  ", "  /___\\  "])]
        frame_index = trader_panel.get("frame_index", 0) % len(frames)
        face = frames[frame_index]
        for index, line in enumerate(face):
            text = self.font.render(line, True, (255, 255, 255))
            screen.blit(text, (x, y + index * 16))

        name = trader_panel.get("name", "Trader\n")
        text = self.font.render(name, True, (255, 215, 0))
        screen.blit(text, (x, y + 5 * 16))

        current_y = y + 7 * 16
        if trader_panel.get("message"):
            for line in str(trader_panel["message"]).splitlines():
                text = self.font.render(line, True, (255, 255, 255))
                screen.blit(text, (x, current_y))
                current_y += 16
            current_y += 32

        options = trader_panel.get("options", [])
        for index, option in enumerate(options):
            text = self.font.render(f"{index + 1}. {option}", True, (0, 255, 0))
            screen.blit(text, (x, current_y + index * 16))
        current_y += len(options) * 16

        if trader_panel.get("details"):
            for index, line in enumerate(trader_panel["details"]):
                for subline in str(line).splitlines():
                    text = self.font.render(subline, True, (255, 255, 255))
                    screen.blit(text, (x, current_y))
                    current_y += 16
