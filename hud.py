# hud.py
import pygame
from settings import *


class HUD:
    def __init__(self, font_big, font_small):
        self.font_big = font_big
        self.font_small = font_small

    def draw(self, surface, player, kills, wave):
        # Fundo semitransparente no topo
        bar = pygame.Surface((SCREEN_WIDTH, 36), pygame.SRCALPHA)
        bar.fill((10, 10, 30, 200))
        surface.blit(bar, (0, 0))

        # Kills
        kills_txt = self.font_small.render(f"INIMIGOS: {kills}/{WIN_KILLS}", True, NEON_CYAN)
        surface.blit(kills_txt, (14, 8))

        # Vida (corações)
        hp_label = self.font_small.render("VIDA:", True, NEON_PINK)
        surface.blit(hp_label, (SCREEN_WIDTH // 2 - 80, 8))
        for i in range(PLAYER_HP):
            color = NEON_PINK if i < player.hp else DARK_GRAY
            pygame.draw.polygon(surface, color, self._heart_points(SCREEN_WIDTH // 2 - 20 + i * 28, 18))

        # Wave
        wave_txt = self.font_small.render(f"WAVE {wave}", True, NEON_YELLOW)
        surface.blit(wave_txt, (SCREEN_WIDTH - 110, 8))

    def _heart_points(self, cx, cy):
        # Coração simplificado com polígono
        return [
            (cx, cy + 8),
            (cx - 10, cy - 2),
            (cx - 10, cy - 8),
            (cx - 5, cy - 10),
            (cx, cy - 6),
            (cx + 5, cy - 10),
            (cx + 10, cy - 8),
            (cx + 10, cy - 2),
        ]
