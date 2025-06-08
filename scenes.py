import pygame
import sys
import random
import math
from constants import *

class Letter:
    def __init__(self, char, final_pos):
        self.char = char
        self.final_pos = pygame.Vector2(final_pos)
        angle = random.uniform(0, 2 * math.pi)
        distance = max(SCREEN_WIDTH, SCREEN_HEIGHT) * 1.2
        self.pos = pygame.Vector2(
            SCREEN_WIDTH / 2 + math.cos(angle) * distance,
            SCREEN_HEIGHT / 2 + math.sin(angle) * distance
        )
        self.surface = pygame.font.Font(None, 128).render(char, True, (255, 255, 255))
        self.direction = (self.final_pos - self.pos).normalize() * 10
        self.phase = "in"

    def update(self):
        if self.phase == "in":
            direction = self.final_pos - self.pos
            self.pos += direction * 0.03
            if direction.length_squared() < 2:
                self.pos = self.final_pos
                self.phase = "pause"
                self.pause_timer = 30  # frames
        elif self.phase == "pause":
            self.pause_timer -= 1
            if self.pause_timer <= 0:
                angle = random.uniform(0, 2 * math.pi)
                self.direction = pygame.Vector2(math.cos(angle), math.sin(angle)) * 10
                self.phase = "out"
        elif self.phase == "out":
            self.pos += self.direction

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

    def is_off_screen(self):
        return not (0 <= self.pos.x <= SCREEN_WIDTH and 0 <= self.pos.y <= SCREEN_HEIGHT)

def run_intro(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 128)
    word = "Asteroids"
    width = sum(font.size(c)[0] for c in word)
    x = SCREEN_WIDTH // 2 - width // 2
    final_positions = []
    for c in word:
        w, h = font.size(c)
        final_positions.append((x, SCREEN_HEIGHT // 2 - h // 2))
        x += w

    letters = [Letter(c, pos) for c, pos in zip(word, final_positions)]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        all_off_screen = True
        for letter in letters:
            letter.update()
            letter.draw(screen)
            if letter.phase != "out" or not letter.is_off_screen():
                all_off_screen = False

        pygame.display.flip()
        clock.tick(60)

        if all_off_screen:
            done = True
