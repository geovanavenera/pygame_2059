# enemy.py
import pygame
import random
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 34
        self.height = 50
        self.image = self._build_image()
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + random.randint(0, 80)
        self.rect.bottom = FLOOR_Y
        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        self.hp = ENEMY_HP
        self.hit_flash = 0

    def _build_image(self):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Corpo
        pygame.draw.rect(surf, NEON_PINK, (7, 18, 20, 20))
        # Cabeça (robótica)
        pygame.draw.rect(surf, NEON_PINK, (8, 3, 18, 15))
        # Olho vermelho (ciclope)
        pygame.draw.circle(surf, NEON_RED, (17, 11), 5)
        pygame.draw.circle(surf, (255, 100, 100), (17, 11), 3)
        # Pernas
        pygame.draw.rect(surf, DARK_GRAY, (7, 38, 8, 12))
        pygame.draw.rect(surf, DARK_GRAY, (19, 38, 8, 12))
        # Braços
        pygame.draw.rect(surf, NEON_PINK, (0, 20, 7, 6))
        pygame.draw.rect(surf, NEON_PINK, (27, 20, 7, 6))
        # Contorno
        pygame.draw.rect(surf, NEON_RED, (7, 18, 20, 20), 1)
        pygame.draw.rect(surf, NEON_RED, (8, 3, 18, 15), 1)
        return surf

    def take_damage(self):
        self.hp -= 1
        self.hit_flash = 10
        if self.hp <= 0:
            self.kill()
            return True
        return False

    def update(self):
        self.rect.x -= self.speed
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.rect.right < 0:
            self.kill()

    def draw(self, surface):
        if self.hit_flash > 0 and self.hit_flash % 2 == 0:
            # Flash branco ao levar dano
            flash = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 180))
            surface.blit(self.image, self.rect)
            surface.blit(flash, self.rect)
        else:
            surface.blit(self.image, self.rect)
        self._draw_hp_bar(surface)

    def _draw_hp_bar(self, surface):
        bar_w = 34
        bar_h = 4
        x = self.rect.x
        y = self.rect.top - 8
        pygame.draw.rect(surface, NEON_RED, (x, y, bar_w, bar_h))
        filled = int(bar_w * (self.hp / ENEMY_HP))
        pygame.draw.rect(surface, NEON_ORANGE, (x, y, filled, bar_h))
        pygame.draw.rect(surface, WHITE, (x, y, bar_w, bar_h), 1)
