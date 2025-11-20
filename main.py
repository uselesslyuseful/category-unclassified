import pygame
from pygame.locals import *
from classes import Player, Object

pygame.init()

SCREEN_WIDTH = 1080
WORLD_WIDTH = 5200
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

player = Player("PlayerSideStillScaled.png", 90, 540, 5)
background_image = pygame.image.load("background.png").convert()


all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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

    # --- CAMERA LOGIC ---
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))

    # --- DRAW ---
    screen.blit(background_image, (-camera_x, 0))

    # Draw each sprite with camera offset
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
