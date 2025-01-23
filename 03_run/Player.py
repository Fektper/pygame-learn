import pygame
import os

GRAVITY = 0.005

class Player:
    def __init__(self, pos: pygame.Rect):
        self.pos = pos
        self.ground = pos.y
        self.internal_timer = 0
        self.up_velocity = 0
        self.pose_length = 1000 // 8

        image_paths = [os.path.join("char", x) for x in os.listdir("char") if x.endswith(".png")]
        self.images = [pygame.image.load(i).convert() for i in image_paths]

    def draw(self, surface: pygame.Surface):
        i = self.internal_timer // self.pose_length % len(self.images)

        surface.blit(self.images[i], self.pos)

    def update(self, keys, dt):
        self.internal_timer += dt
        while self.internal_timer >= self.pose_length * len(self.images):
            self.internal_timer -= self.pose_length * len(self.images)

        if keys[pygame.K_SPACE] and self.pos.y == self.ground:
            self.up_velocity = 2
        elif self.pos.y >= self.ground:
            self.pos.y = self.ground
            self.up_velocity = 0

        self.pos.y -= self.up_velocity * dt
        
        self.up_velocity -= GRAVITY * dt