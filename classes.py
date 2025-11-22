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
            self.rect.y += self.dir
            if abs(self.rect.y - self.ogy_pos) >= self.lim:
                # clamp to limit to avoid overshoot
                if self.dir == 1:
                    self.rect.y = self.ogy_pos + self.lim
                else:
                    self.rect.y = self.ogy_pos - self.lim
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
    def analyze_object(self, obj):
        analyzer_popup = Decoration("Analyzer_Popup.png", self.rect.centerx, self.rect.centery - 450, 2, 50)

        font = pygame.font.Font('freesansbold.ttf', 18)

        # Wrap BOTH title and description
        title_lines = Station.render_text_wrapped(obj.name, font, (255,255,255), 400)
        desc_lines  = Station.render_text_wrapped(obj.desc,  font, (255,255,255), 400)

        analyzer_rends = title_lines + desc_lines

        # Build rects with spacing
        analyzer_rects = []
        base_y = analyzer_popup.rect.centery + 130
        for i, rend in enumerate(analyzer_rends):
            rect = rend.get_rect(center=(
                analyzer_popup.rect.centerx,
                base_y + i * 30
            ))
            analyzer_rects.append(rect)

        return analyzer_popup, analyzer_rends, analyzer_rects

    @staticmethod
    def render_text_wrapped(text, font, color, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        # Turn lines into Surfaces
        rendered_lines = [font.render(line, True, color) for line in lines]
        return rendered_lines
