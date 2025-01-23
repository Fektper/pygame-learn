import pygame
from Player import Player


pygame.init()
screen = pygame.display.set_mode((1024, 720))
clock = pygame.time.Clock()

running = True
dt = 0

player = Player(pygame.Rect(500, 500, 100, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # Update screen
    screen.fill("white")
    player.draw(screen)
    pygame.display.flip()

    player.update(pygame.key.get_just_pressed(), dt)


    dt = clock.tick(60)