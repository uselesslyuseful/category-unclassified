import pygame
from pygame.locals import *

WORLD_WIDTH = 5200
SCREEN_HEIGHT = 720

class Object(pygame.sprite.Sprite):
    pass


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
