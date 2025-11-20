import pygame
from pygame.locals import *
from classes import Player, Object, Station

pygame.init()

SCREEN_WIDTH = 1080
WORLD_WIDTH = 5200
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

player = Player("PlayerSideStillScaled.png", 90, 540, 5)
background_image = pygame.image.load("background.png").convert()
objects_one = [Object("A Coffee Mug that Pours Upside-Down", "A coffee mug that defies gravity. Leave it alone for too long and it just might spill over.", "ScaledCoffee.png", 1)]
analyzer = Station("Analyzer.png", 1100, 400, "analyzer")

objects = pygame.sprite.Group()
for sprite in objects_one:
    objects.add(sprite)

stations = pygame.sprite.Group()
stations.add(analyzer)

frame = 0
running = True
while running:
    for event in pygame.event.get(): 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update_pos(pressed_keys)
    for object in objects_one:
        object.update(frame)

    # --- CAMERA LOGIC ---
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))

    # --- DRAW ---
    screen.blit(background_image, (-camera_x, 0))

    for station in stations:
        screen.blit(station.image, (station.rect.x - camera_x, station.rect.y))

    for sprite in objects:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
    
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

    pygame.display.update()
    frame += 1
    clock.tick(60)

pygame.quit()
