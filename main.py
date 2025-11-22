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
background_image = pygame.image.load("working_bg.png").convert()
objects_one = [
    Object(
        "A Coffee Mug that Pours Upside-Down",
        "A coffee mug that defies gravity...",
        "ScaledCoffee.png",
        3,
        ["synthetic", "gravity-defying"],
        analysis_data={
            "material": "Porcelain anomaly",
            "density": "0.75g/mL",
            "instability": 100,
            "temperature": "Lukewarm",
            "danger_level": "Low"
        }
    )
]

analyzer = Station("Analyzer.png", 900, 700, "analyzer")
conveyor = Station("conveyor.png", 0, 720, "conveyor")
conveyor_origin = Station("Conveyor_origin.png", 0, 680, "conveyor_origin")

objects = pygame.sprite.Group()
for sprite in objects_one:
    objects.add(sprite)

stations = pygame.sprite.Group()
stations.add(analyzer)
stations.add(conveyor)


decorations = pygame.sprite.Group()

analyzer_rends, analyzer_rects = [], []

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
        if object.state == "analysis":
            analyzer_pop_up, analyzer_rends, analyzer_rects = analyzer.analyze_object(object)
            decorations.add(analyzer_pop_up)
            object.state = "analysis_complete"
            

    # --- CAMERA LOGIC ---
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))

    # --- DRAW ---
    screen.blit(background_image, (-camera_x, 0))

    for station in stations:
        screen.blit(station.image, (station.rect.x - camera_x, station.rect.y))

    for sprite in objects:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
    
    screen.blit(conveyor_origin.image, (conveyor_origin.rect.x - camera_x, conveyor_origin.rect.y))
    
    for sprite in decorations:
        sprite.animate(frame)
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
    
    if analyzer_rects:
        for rend, rect in zip(analyzer_rends, analyzer_rects):
            if frame % analyzer_pop_up.spd == 0:
                rect.y += analyzer_pop_up.dir
            screen.blit(rend, (rect.x - camera_x, rect.y))

    
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

    pygame.display.update()
    frame += 1
    clock.tick(60)

pygame.quit()
