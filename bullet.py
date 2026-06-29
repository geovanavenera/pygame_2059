import pygame
from settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.image = pygame.Surface((14, 5), pygame.SRCALPHA)
        pygame.draw.rect(self.image, NEON_YELLOW, (0, 0, 14, 5))
        pygame.draw.rect(self.image, WHITE, (0, 0, 14, 5), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.centery = y

    def update(self):
        self.rect.x += BULLET_SPEED * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
