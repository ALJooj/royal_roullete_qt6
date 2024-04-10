import os
import pygame
import sys
from functions_pygame import load_image

tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# print(pygame.font.get_fonts())

pygame.font.init()
font = pygame.font.SysFont('arial', 40)

blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# tile_width = tile_height = 100


class Dot(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, *sprites):
        super().__init__(sprites)
        self.image = pygame.transform.scale(load_image('dot.png', -1), (15, 15))  # рандомное заполнение
        self.rect = self.image.get_rect().move(x, y)
        # self.rect = pygame.Rect(x, y, w, h)

    def move(self, pos):
        self.rect = self.rect.move(pos[0], pos[1])

    def can_be_placed(self, group_dots):
        for sprite in group_dots:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.rect.colliderect(sprite.rect):
                return True
        return False


class Chip(pygame.sprite.Sprite):
    def __init__(self, x, y, *sprites):
        super().__init__(sprites)
        self.cost = 10
        self.image = pygame.transform.scale(load_image('chip.png', -1), (50, 50))
        self.rect = self.image.get_rect().move(x - 25, y - 25)

    def check_state(self, kill=False):
        if kill:
            self.kill()

    def update(self, btn_start_pressed=False):
        if btn_start_pressed:
            self.kill()


class GridOfDots(pygame.surface.Surface):
    def __init__(self, offset, *sprites):
        super().__init__((989, 562), )

        self.tile_height = 53
        self.tile_width = 87
        # self.image = pygame.transform.scale(load_image('fishka.png', -1), (50, 50))
        # self.rect = self.image.get_rect().move(x, y)
        for i in range(4):
            for j in range(13):
                Dot(offset[0] + (self.tile_height * j), offset[1] + (self.tile_width * i), sprites)


class TileRect(pygame.sprite.Sprite):
    def __init__(self, x, y, number, color, *sprites):
        super().__init__(sprites)
        self.number = number
        self.value = 0
        self.color = color
        self.image = pygame.transform.scale(load_image('brick.png', -1), (53, 85))
        self.rect = self.image.get_rect().move(x, y)

    def can_be_placed(self, group):
        for sprite in group:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and self.rect.colliderect(sprite.rect):
                return True

        return False

    def bet(self, value):
        self.value += value


class GridOfTiles(pygame.surface.Surface):
    def __init__(self, offset, *sprites):
        super().__init__((989, 562))
        self.tile_height = 53
        self.tile_width = 85
        for i in range(3):
            for j in range(12):
                TileRect(offset[0] + (self.tile_height * j), offset[1] + (self.tile_width * i),
                         abs(i - 3) + (3 * j),
                         'b' if abs(i - 3) + (3 * j) in blacks else 'r',
                         sprites)


class Button:
    def __init__(self, color, x, y, width, height, text='', on_click=object):
        self.func = on_click
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text,
                 (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def on_click(self, pos, *args):
        if pygame.rect.Rect(self.x, self.y, self.width, self.height).collidepoint(pos):
            return self.func(*args)