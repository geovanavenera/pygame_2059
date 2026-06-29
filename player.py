# player.py
import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 36
        self.height = 56
        self.image = self._build_image()
        self.rect = self.image.get_rect()
        self.rect.x = 80
        self.rect.bottom = FLOOR_Y

        self.vel_y = 0
        self.on_ground = True
        self.hp = PLAYER_HP
        self.invincible = 0   # frames de invencibilidade após levar dano
        self.facing = 1       # 1 = direita, -1 = esquerda
        self.shoot_cooldown = 0

    def _build_image(self):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Corpo (tronco)
        pygame.draw.rect(surf, NEON_CYAN, (8, 20, 20, 22))
        # Cabeça
        pygame.draw.rect(surf, NEON_CYAN, (9, 4, 18, 16))
        # Viseira (capacete)
        pygame.draw.rect(surf, NEON_PINK, (11, 7, 14, 8))
        # Pernas
        pygame.draw.rect(surf, DARK_GRAY, (8, 42, 8, 14))
        pygame.draw.rect(surf, DARK_GRAY, (20, 42, 8, 14))
        # Braço com arma
        pygame.draw.rect(surf, NEON_CYAN, (28, 24, 8, 6))
        # Cano da arma
        pygame.draw.rect(surf, NEON_YELLOW, (32, 25, 6, 4))
        # Contorno neon
        pygame.draw.rect(surf, NEON_CYAN, (8, 20, 20, 22), 1)
        pygame.draw.rect(surf, NEON_CYAN, (9, 4, 18, 16), 1)
        return surf

    def handle_input(self, keys):
        # Movimento horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            self.facing = 1

        # Pulo
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = PLAYER_JUMP
            self.on_ground = False

        # Limitar dentro da tela
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.width))

    def try_shoot(self):
        """Retorna uma bala se o cooldown permitir, senão None."""
        from bullet import Bullet
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = 18
            bx = self.rect.right if self.facing == 1 else self.rect.left
            return Bullet(bx, self.rect.centery - 4, self.facing)
        return None

    def take_damage(self):
        if self.invincible <= 0:
            self.hp -= 1
            self.invincible = 90  # ~1.5 segundos de invencibilidade

    def update(self):
        # Gravidade
        self.vel_y += PLAYER_GRAVITY
        self.rect.y += self.vel_y

        # Chão
        if self.rect.bottom >= FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.vel_y = 0
            self.on_ground = True

        # Cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1

    def draw(self, surface):
        # Pisca quando invencível
        if self.invincible > 0 and (self.invincible // 6) % 2 == 0:
            return
        img = self.image
        if self.facing == -1:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, self.rect)
        self._draw_hp_bar(surface)

    def _draw_hp_bar(self, surface):
        bar_w = 40
        bar_h = 5
        x = self.rect.x - 2
        y = self.rect.top - 10
        pygame.draw.rect(surface, NEON_RED, (x, y, bar_w, bar_h))
        filled = int(bar_w * (self.hp / PLAYER_HP))
        pygame.draw.rect(surface, NEON_CYAN, (x, y, filled, bar_h))
        pygame.draw.rect(surface, WHITE, (x, y, bar_w, bar_h), 1)
