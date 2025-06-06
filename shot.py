import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
   
    def __init__(self, position, rotation):
        super().__init__(position[0], position[1], SHOT_RADIUS)
        self.velocity = pygame.Vector2(0,1).rotate(rotation) * PLAYER_SHOOT_SPEED
        self.rotation = rotation
        self.SHOT_RADIUS = SHOT_RADIUS
        
        

    def draw(self, screen):
        pos = (round(self.position[0]), round(self.position[1]))
        pygame.draw.circle(screen, "white", pos, self.SHOT_RADIUS, width = 2)

    def update(self, dt):
        self.position += (self.velocity * dt)