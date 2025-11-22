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
        self.analyzed = False
    def update(self, frame):
        if self.onConveyor:
            if frame % 2 == 0:
                self.rect.x += self.spd
        if self.rect.centerx >= 1100 and not self.analyzed:
            self.onConveyor = False
            self.analyze = True

class Decoration(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, spd, lim):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.ogy_pos = y_pos
        self.spd = spd
        self.lim = lim
        self.dir = 1
    def animate(self, frame):
        if frame % self.spd == 0:
            if self.dir == 1:
                self.rect.y += 1
            else:
                self.rect.y -= 1
            if self.rect.y == self.ogy_pos + self.lim or self.rect.y == self.ogy_pos - self.lim:
                self.dir *= -1

        

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
        analyzer_popup = Decoration("Analyzer_Popup.png", self.rect.centerx, self.rect.centery + 50, 2, 20)
        analyzer_text = [object.name, object.desc]
        font = pygame.font.Font('freesansbold.ttf', 25)
        analyzer_rends = [font.render(text, True, (255,255,255)) for text in analyzer_text]
        analyzer_rects = [rend.get_rect(center = (analyzer_popup.rect.centerx, analyzer_popup.rect.centery)) for rend in analyzer_rends]
        return analyzer_popup, analyzer_rends, analyzer_rects