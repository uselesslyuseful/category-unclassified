import pygame
from pygame.locals import *

WORLD_WIDTH = 5200
SCREEN_HEIGHT = 720

class Object(pygame.sprite.Sprite):
    def __init__(self, name, desc, image, spd):
        super().__init__()
        self.name = name
        self.desc = desc
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (200, 550))
        self.onConveyor = True
        self.spd = spd
        self.analyze = False
    def update(self, frame):
        if self.onConveyor:
            if frame % 2 == 0:
                self.rect.x += self.spd
        if self.rect.centerx >= 1100:
            self.onConveyor = False
            self.analyze = True

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, spd):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.spd = spd
    
    def update_pos(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.x -= self.spd
        if pressed_keys[K_RIGHT]:
            self.rect.x += self.spd
        
        # clamp within WORLD width
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - self.rect.width))

class Station(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, type):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.type = type
    def analyze_object(self, object):
        pass