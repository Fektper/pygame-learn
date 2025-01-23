import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running=True
dt = 0

player_radius = 20
player_speed = 1.0
player_speed_basefactor = 300
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_dir = pygame.Vector2(1, 1)

boing_sound = pygame.mixer.Sound("boing_sound.wav")
boing_sound.fadeout(100)

while running:
    # vent polling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, player_radius)

    hit = False
    if player_pos.y - player_radius <= 0 and player_dir.y < 0:
        player_dir.y = -player_dir.y
        hit = True
    if player_pos.y + player_radius >= screen.get_height() and player_dir.y > 0:
        player_dir.y = -player_dir.y
        hit = True
    if player_pos.x - player_radius <= 0 and player_dir.x < 0:
        player_dir.x = -player_dir.x
        hit = True  
    if player_pos.x + player_radius >= screen.get_width() and player_dir.x > 0:
        player_dir.x = -player_dir.x
        hit = True

    if hit:
        player_speed = player_speed + 0.1
        player_radius = player_radius + 5
        boing_sound.play()
        # Fix pop at end
        boing_sound.fadeout(int(boing_sound.get_length()*1000) - 5)
    player_pos = player_pos + (player_dir / player_dir.magnitude()) * player_speed * dt * player_speed_basefactor

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()