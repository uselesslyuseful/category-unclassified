import pygame
from pygame.locals import *

WORLD_WIDTH = 5200
SCREEN_HEIGHT = 720

class Object(pygame.sprite.Sprite):
    def __init__(self, name, desc, image, spd, tags, analysis_data, integrity = 100, instability = 0, mass = 1, value = 1):
        super().__init__()
        self.name = name
        self.desc = desc
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (0, 550))
        self.spd = spd
        self.state = "onConveyor"
        self.tags = tags
        self.instability = instability
        self.integrity = integrity
        self.mass = mass
        self.analysis_data = analysis_data
        self.value = value
    def update(self, frame):
        if self.state == "onConveyor":
            if frame % 2 == 0:
                self.rect.x += self.spd
        if self.rect.centerx >= 1100 and not self.state == "analysis_complete":
            self.state = "analysis"

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
        self.rect = self.image.get_rect(bottomleft = (x_pos, y_pos))
        self.type = type
    def analyze_object(self, obj):
        analyzer_popup = Decoration("Analyzer_Popup.png", self.rect.centerx - 15, self.rect.centery - 430, 2, 20)
        title_font = pygame.font.Font('freesansbold.ttf', 18)
        font = pygame.font.Font('freesansbold.ttf', 15)

        # Wrap BOTH title and description
        title_lines = Station.render_text_wrapped(obj.name, title_font, (255,255,255), 400)
        desc_lines  = Station.render_text_wrapped(obj.desc,  font, (255,255,255), 400)
        analysis_lines = []
        for key, value in obj.analysis_data.items():
            line = f"{key.capitalize()}: {value}"
            analysis_lines.append(line)
        analysis_rends = [font.render(line, True, (255,255,255)) for line in analysis_lines]

        analyzer_rends = title_lines + desc_lines + analysis_rends

        # Build rects with spacing
        analyzer_rects = []
        base_y = analyzer_popup.rect.centery + 100
        for i, rend in enumerate(analyzer_rends):
            rect = rend.get_rect(center=(
                analyzer_popup.rect.centerx,
                base_y + i * 18
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
