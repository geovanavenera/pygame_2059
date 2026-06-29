# main.py — 2059: Survive the Chrome City
import pygame
import sys
import random
import math

from settings import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from hud import HUD
from menu import Menu


def draw_background(surface, tick, buildings_bg):
    """Renderiza o cenário cyberpunk."""
    surface.fill(DARK_BG)

    # Grade no fundo
    for x in range(0, SCREEN_WIDTH, 50):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    # Prédios do fundo (parallax lento)
    for b in buildings_bg:
        b["x"] -= b["speed"]
        if b["x"] + b["w"] < 0:
            b["x"] = SCREEN_WIDTH + random.randint(0, 60)
            b["h"] = random.randint(60, 200)
        pygame.draw.rect(surface, (12, 12, 30), (b["x"], FLOOR_Y - b["h"], b["w"], b["h"]))
        pygame.draw.rect(surface, NEON_CYAN, (b["x"], FLOOR_Y - b["h"], b["w"], b["h"]), 1)
        # janelas
        for wy in range(FLOOR_Y - b["h"] + 8, FLOOR_Y - 8, 14):
            for wx in range(int(b["x"]) + 5, int(b["x"]) + b["w"] - 5, 12):
                if (wx + wy + tick // 30) % 3 != 0:
                    c = NEON_CYAN if (wx * wy) % 2 == 0 else NEON_PINK
                    pygame.draw.rect(surface, c, (wx, wy, 5, 4))

    # Chão neon
    pygame.draw.rect(surface, (20, 20, 50), (0, FLOOR_Y, SCREEN_WIDTH, FLOOR_HEIGHT))
    pygame.draw.line(surface, NEON_CYAN, (0, FLOOR_Y), (SCREEN_WIDTH, FLOOR_Y), 2)
    # Linhas de perspectiva no chão
    for i in range(0, SCREEN_WIDTH, 60):
        offset = (tick + i * 3) % SCREEN_WIDTH
        pygame.draw.line(surface, (0, 60, 80), (offset, FLOOR_Y), (offset, SCREEN_HEIGHT), 1)


def show_endscreen(surface, font_big, font_med, font_small, won, kills):
    clock = pygame.time.Clock()
    tick = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "menu"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        surface.fill(DARK_BG)

        # Grade
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))

        if won:
            glow = int(150 + 105 * math.sin(tick * 0.06))
            title = font_big.render("MISSÃO CONCLUÍDA", True, (0, glow, glow))
            msg = font_med.render("Você sobreviveu ao Chrome City.", True, NEON_CYAN)
        else:
            glow = int(150 + 105 * math.sin(tick * 0.06))
            title = font_big.render("GAME OVER", True, (glow, 0, 0))
            msg = font_med.render("Os androides venceram.", True, NEON_PINK)

        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 160)))
        surface.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, 240)))

        kills_txt = font_med.render(f"Inimigos eliminados: {kills}", True, NEON_YELLOW)
        surface.blit(kills_txt, kills_txt.get_rect(center=(SCREEN_WIDTH // 2, 300)))

        alpha = int(128 + 127 * math.sin(tick * 0.07))
        prompt = font_small.render("ENTER — Menu   |   ESC — Sair", True, WHITE)
        prompt.set_alpha(alpha)
        surface.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, 390)))

        pygame.display.flip()
        clock.tick(FPS)
        tick += 1


def game_loop(screen, font_big, font_med, font_small):
    clock = pygame.time.Clock()

    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    hud = HUD(font_big, font_small)

    # Prédios de fundo (parallax)
    buildings_bg = []
    x = 0
    while x < SCREEN_WIDTH:
        w = random.randint(50, 100)
        h = random.randint(60, 200)
        buildings_bg.append({"x": x, "w": w, "h": h, "speed": random.uniform(0.3, 0.8)})
        x += w + random.randint(4, 12)

    kills = 0
    wave = 1
    spawn_timer = 0
    current_spawn_interval = SPAWN_INTERVAL
    tick = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        tick += 1

        # Aumenta dificuldade a cada 5 kills
        wave = kills // 5 + 1
        current_spawn_interval = max(30, SPAWN_INTERVAL - wave * 8)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        keys = pygame.key.get_pressed()
        player.handle_input(keys)

        # Atirar (CTRL esquerdo ou direito)
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            bullet = player.try_shoot()
            if bullet:
                bullets.add(bullet)

        player.update()
        bullets.update()

        # Spawn de inimigos
        spawn_timer += 1
        if spawn_timer >= current_spawn_interval:
            spawn_timer = 0
            enemies.add(Enemy())

        enemies.update()

        # Colisão bala x inimigo
        for bullet in list(bullets):
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                bullet.kill()
                killed = enemy.take_damage()
                if killed:
                    kills += 1

        # Colisão inimigo x jogador
        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                player.take_damage()

        # Inimigos passando pela tela (chegaram no fim)
        for enemy in list(enemies):
            if enemy.rect.right < 0:
                enemy.kill()

        # Desenhar
        draw_background(screen, tick, buildings_bg)

        for enemy in enemies:
            enemy.draw(screen)

        for bullet in bullets:
            screen.blit(bullet.image, bullet.rect)

        player.draw(screen)
        hud.draw(screen, player, kills, wave)

        # Condição de vitória
        if kills >= WIN_KILLS:
            return show_endscreen(screen, font_big, font_med, font_small, True, kills)

        # Condição de derrota
        if player.hp <= 0:
            return show_endscreen(screen, font_big, font_med, font_small, False, kills)

        pygame.display.flip()

    return "menu"


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    # Fontes
    font_big   = pygame.font.SysFont("consolas", 52, bold=True)
    font_med   = pygame.font.SysFont("consolas", 22)
    font_small = pygame.font.SysFont("consolas", 16)

    state = "menu"
    while True:
        if state == "menu":
            menu = Menu(screen, font_big, font_med, font_small)
            state = menu.run()
        elif state == "play":
            state = game_loop(screen, font_big, font_med, font_small)
        elif state == "quit":
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
