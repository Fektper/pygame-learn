import pygame
from Scenes import MenuScene
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720


pygame.init()
pygame.display.set_caption("TicTacGo!")
logo = pygame.image.load("logo/logo64.png")
pygame.display.set_icon(logo)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()
target_fps = 60
clock = pygame.Clock()
dt = 0

running = True

activeScene = MenuScene(SCREEN_WIDTH, SCREEN_HEIGHT)

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            break
    
    activeScene.update(events, dt)
    # Render
    screen.fill("white")
    # Render here
    activeScene.render(screen)
    # Render end
    pygame.display.flip()



    dt = clock.tick(target_fps) / 1000


pygame.quit()