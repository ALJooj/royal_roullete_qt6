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

# до запуска
fon = pygame.transform.scale(load_image('start_fon.png'), (790, 450))
grid_of_tiles = GridOfTiles((75, 26), brick_group, all_sprites)
grid_of_dots = GridOfDots((71, 15), tiles_group, all_sprites)
grid_of_bets = GridOfBets((75, 270), brick_group, all_sprites)

screen.blit(grid_of_dots, (0, 0))
screen.blit(grid_of_tiles, (0, 0))
screen.blit(fon, (0, 0))

cont = False

my_wallet = 350
last_win_pos = 0
last_win_bet = 0
history_tiles = []
history_bets = []
history_win_tiles = []
history_win_bets = []

blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]


def repeat_last_roll(bets, poses, screen, tiles, chips, wallet, bet_grid):
    # for tile in tiles:
    #     if tile
    # print(poses, bets)
    delta = wallet
    for tile in tiles:
        if wallet > 0:
            for i in range(len(poses[-1])):
                if i == tile.number:
                    for j in range(len(bets[-1])):
                        for k in range(bets[-1][j] // 10):
                            a = Chip(tile.rect.x + 28, tile.rect.y + 42, chips_group, all_sprites)
                            # for i in range()
                            print('bets', bets)
                            tile.bet(a.cost)
                            delta -= a.cost

            # if tile.number in poses[-1]:
            #     a = Chip(tile.rect.x + 28, tile.rect.y + 42, chips_group, all_sprites)
            #     # for i in range()
            #     print('bets', bets)
            #     tile.bet(a.cost)
            #     delta -= a.cost
    delta -= wallet
    print('wallet', delta)
    return delta


def randomize_roll(tiles, chips, wallet, bet_grid):
    position = random.randint(0, 36)
    win_val = 0
    local_his_bet_poses = []
    last_bets = []
    # position = 13
    for tile in tiles:
        if tile.value != 0:
            local_his_bet_poses.append(tile.number)
            last_bets.append(tile.value)

        # if tile.number in range(100, 109):
        if tile.value > 0:
            # если совпал номер
            if tile.number in range(0, 37) and position == tile.number:
                win_val += tile.value * 36

            # в первых 12 (1:3)
            if tile.number in range(100, 103):
                if position in range(1, 13) and tile.number == 100:
                    win_val += tile.value * 3
                if position in range(13, 25) and tile.number == 101:
                    win_val += tile.value * 3
                if position in range(25, 37) and tile.number == 102:
                    win_val += tile.value * 3
                # win_val += tile.value * 3

            if tile.number in range(103, 109):
                # 1-19
                if tile.number == 103 and position in range(1, 19):
                    win_val += tile.value * 2

                if tile.number == 108 and position in range(19, 37):
                    win_val += tile.value * 2

                # odd or even
                if tile.number == 104 and position % 2 == 0:
                    win_val += tile.value * 2

                if tile.number == 107 and position % 2 == 1:
                    win_val += tile.value * 2

                # red or black
                if tile.number == 105 and position not in blacks:
                    win_val += tile.value * 2

                if tile.number == 106 and position in blacks:
                    win_val += tile.value * 2

            tile.value = 0
        tile.value = 0

    for c in chips:
        c.rect = c.rect.move(1000, 1000)
        c.update(True)
        c.kill()
    for c in all_sprites:
        if type(c) is Chip:
            c.rect = c.rect.move(1000, 1000)
            c.update(True)
            c.kill()

    return position, win_val, tuple(local_his_bet_poses), tuple(last_bets)


# color, x, y, width, height, text=''
start_btn = Button((255, 255, 255), 800, 80, 140, 140, 'start', randomize_roll)
repeat_btn = Button((255, 255, 255), 800, 240, 140, 140, 'repeat', repeat_last_roll)




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
            b = repeat_btn.on_click(event.pos, history_bets, history_tiles, screen, brick_group, chips_group, my_wallet, grid_of_bets)
            my_wallet += b if b is not None else 0
            a = start_btn.on_click(event.pos, brick_group, chips_group, my_wallet, grid_of_bets)
            if a is None:
                pass
            else:
                print(a)
                last_win_pos, last_win_bet, last_bet_poses, last_bets_of_poses = a
                my_wallet += last_win_bet
                history_bets.append(last_bets_of_poses)
                history_tiles.append(last_bet_poses)
                history_win_tiles.append(last_win_pos)
                history_win_bets.append(last_win_bet)

            for chip in chips_group:
                chip.update()

            for tile in tiles_group:
                if tile.can_be_placed(brick_group):
                    if my_wallet > 0:
                        a = Chip(tile.rect.center[0], tile.rect.center[1], chips_group, all_sprites)
                        tile.bet(a.cost)
                        my_wallet -= a.cost
                        cont = True     # 1 клик 1 ставка

            if cont:
                cont = False
                continue

            for tile in brick_group:
                if tile.can_be_placed(tiles_group):
                    if my_wallet > 0:
                        a = Chip(tile.rect.x + 28, tile.rect.y + 42, chips_group, all_sprites)
                        tile.bet(a.cost)
                        my_wallet -= a.cost
            clicked = True

    font_1 = pygame.font.SysFont('castellar', 44)
    string_rendered = font_1.render('Bank: ' + str(my_wallet),
                                    1, pygame.Color('red'))
    string_rendered_2 = font_1.render("Победное число " + str(last_win_pos) + (' черное ' if last_win_pos in blacks else
                                      ' красное ') + " ваш выигрыш " + str(last_win_bet),
                                    1, pygame.Color('red'))


    # после отрисовки всего, переворачиваем экран
    screen.fill((255, 255, 255))
    screen.blit(fon, (0, 0))
    start_btn.draw(screen)
    repeat_btn.draw(screen)
    # all_sprites.draw(screen)
    buttons_group.draw(screen)
    brick_group.draw(screen)
    tiles_group.draw(screen)
    chips_group.draw(screen)

    # texts
    screen.blit(string_rendered_2, (50, 600))
    screen.blit(string_rendered, (800, 500))
    clock.tick(FPS)
    pygame.display.flip()


