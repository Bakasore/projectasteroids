import pygame
from circleshape import CircleShape
from constants import *
from shot import *


class Player(CircleShape):
    def __init__(self, x, y, shot_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_group = shot_group
        self.timer = 0
        self.velocity = pygame.Vector2(0, 0)
        self.max_speed = 300
        self.acceleration = 200

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.velocity += forward * self.acceleration * dt
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)

        if keys[pygame.K_s]:
            self.velocity *= -0.95  # slight braking

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_SPACE] and self.timer <= 0:
            self.shoot()

        self.position += self.velocity * dt
        self.wrap_screen()
        self.timer -= dt
        self.timer = max(0, self.timer)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def wrap_screen(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), width=2)

    def shoot(self):
        self.timer = PLAYER_SHOOT_COOLDOWN
        shot_fired = Shot(self.triangle()[0], self.rotation)
        self.shot_group.add(shot_fired)
        return shot_fired
