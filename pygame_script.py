import pygame
import random
from functions_pygame import *
from classes_pygame import *


# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 1090  # ширина игрового окна
HEIGHT = 650 # высота игрового окна
FPS = 30 # частота кадров в секунду

# создаем игру и окно
pygame.init()
# pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Royal Roulette")
clock = pygame.time.Clock()

# groups
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
brick_group = pygame.sprite.Group()
chips_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()

running = True
screen.fill((255,255,255))
# до запуска
fon = pygame.transform.scale(load_image('start_fon.png'), (790, 450))
grid_of_tiles = GridOfTiles((75, 26), brick_group, all_sprites)
grid_of_dots = GridOfDots((71, 15), tiles_group, all_sprites)

screen.blit(grid_of_dots, (0, 0))
screen.blit(grid_of_tiles, (0, 0))
screen.blit(fon, (0, 0))

cont = False


def randomize_roll(tiles, chips):
    a = random.randint(0, 36)
    for tile in tiles:
        if tile.number == a:
            print(123)

    for chip in chips:
        chip.make_kill()
        # chip.kill()
        # all_sprites.remove(chip)
        # chips_group.remove(chip)
    # chips.remove(chips)
    print(chips)
    return a


# color, x, y, width, height, text=''
start_btn = Button((255, 255, 255), 800, 80, 140, 140, 'start', randomize_roll)


while running:
    # events
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            last_pos = event.pos

            # TileRect(event.pos[0], event.pos[1], brick_group)
            start_btn.on_click(event.pos, brick_group, chips_group)

            for tile in tiles_group:
                if tile.can_be_placed(brick_group):
                    print(tile.rect.x - 7)
                    Chip(tile.rect.x + 7, tile.rect.y + 7, chips_group, all_sprites)
                    cont = True     # 1 клик 1 ставка

            if cont:
                cont = False
                continue

            for tile in brick_group:
                if tile.can_be_placed(tiles_group):
                    Chip(tile.rect.x + 28, tile.rect.y + 42, chips_group, all_sprites)
                    print(tile.color, tile. number, type(tile))
            clicked = True

    # после отрисовки всего, переворачиваем экран
    start_btn.draw(screen)
    # all_sprites.draw(screen)
    buttons_group.draw(screen)
    brick_group.draw(screen)
    tiles_group.draw(screen)
    chips_group.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()


