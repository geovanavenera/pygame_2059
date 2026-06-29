# menu.py
import pygame
import math
from settings import *


class Menu:
    def __init__(self, screen, font_big, font_med, font_small):
        self.screen = screen
        self.font_big = font_big
        self.font_med = font_med
        self.font_small = font_small
        self.tick = 0
        self.stars = self._gen_stars()
        self.buildings = self._gen_buildings()

    def _gen_stars(self):
        import random
        return [(random.randint(0, SCREEN_WIDTH), random.randint(0, 260),
                 random.randint(1, 3)) for _ in range(80)]

    def _gen_buildings(self):
        import random
        buildings = []
        x = 0
        while x < SCREEN_WIDTH:
            w = random.randint(40, 90)
            h = random.randint(80, 220)
            buildings.append((x, SCREEN_HEIGHT - h - FLOOR_HEIGHT + 80, w, h))
            x += w + random.randint(2, 8)
        return buildings

    def draw(self):
        self.tick += 1
        self.screen.fill(DARK_BG)
        self._draw_city()
        self._draw_stars()
        self._draw_grid()
        self._draw_title()
        self._draw_controls()
        self._draw_prompt()

    def _draw_stars(self):
        for sx, sy, sr in self.stars:
            brightness = int(150 + 105 * math.sin(self.tick * 0.04 + sx))
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (sx, sy), sr)

    def _draw_city(self):
        for bx, by, bw, bh in self.buildings:
            pygame.draw.rect(self.screen, (15, 15, 35), (bx, by, bw, bh))
            # janelas neon
            for wy in range(by + 8, by + bh - 8, 14):
                for wx in range(bx + 6, bx + bw - 6, 12):
                    if (wx + wy + self.tick // 40) % 3 != 0:
                        color = NEON_CYAN if (wx + wy) % 5 == 0 else NEON_PINK
                        pygame.draw.rect(self.screen, color, (wx, wy, 6, 5))
            pygame.draw.rect(self.screen, NEON_CYAN, (bx, by, bw, bh), 1)

    def _draw_grid(self):
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def _draw_title(self):
        glow = int(180 + 75 * math.sin(self.tick * 0.05))
        title = self.font_big.render("2059", True, (0, glow, glow))
        shadow = self.font_big.render("2059", True, NEON_PINK)
        cx = SCREEN_WIDTH // 2
        self.screen.blit(shadow, shadow.get_rect(center=(cx + 3, 113)))
        self.screen.blit(title, title.get_rect(center=(cx, 110)))

        sub = self.font_med.render("SURVIVE THE CHROME CITY", True, NEON_PINK)
        self.screen.blit(sub, sub.get_rect(center=(cx, 165)))

    def _draw_controls(self):
        cx = SCREEN_WIDTH // 2
        y = 220

        # Caixa de controles
        box = pygame.Surface((360, 130), pygame.SRCALPHA)
        box.fill((0, 0, 0, 160))
        self.screen.blit(box, (cx - 180, y - 10))
        pygame.draw.rect(self.screen, NEON_CYAN, (cx - 180, y - 10, 360, 130), 1)

        header = self.font_small.render("[ CONTROLES ]", True, NEON_YELLOW)
        self.screen.blit(header, header.get_rect(center=(cx, y + 8)))

        controls = [
            ("← → / A D", "Mover"),
            ("SPACE / W / ↑", "Pular"),
            ("CTRL", "Atirar"),
        ]
        for i, (key, action) in enumerate(controls):
            key_surf = self.font_small.render(key, True, NEON_CYAN)
            act_surf = self.font_small.render(f"— {action}", True, WHITE)
            self.screen.blit(key_surf, (cx - 160, y + 32 + i * 26))
            self.screen.blit(act_surf, (cx + 10, y + 32 + i * 26))

    def _draw_prompt(self):
        alpha = int(128 + 127 * math.sin(self.tick * 0.07))
        prompt = self.font_med.render("PRESSIONE ENTER PARA JOGAR", True, NEON_YELLOW)
        prompt.set_alpha(alpha)
        self.screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, 390)))

        esc = self.font_small.render("ESC — Sair", True, GRAY)
        self.screen.blit(esc, esc.get_rect(center=(SCREEN_WIDTH // 2, 430)))

    def run(self):
        """Roda o loop do menu. Retorna 'play' ou 'quit'."""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "play"
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)
