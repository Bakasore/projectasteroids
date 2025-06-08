# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
import random
import math
from constants import *


def run_intro(screen):
    clock = pygame.time.Clock()
    font_main = pygame.font.Font(None, 128)
    font_sub = pygame.font.Font(None, 48)

    word_main = "Asteroids"
    word_sub = "Created by Ben Garza"

    CENTER = screen.get_width() // 2, screen.get_height() // 2

    def get_final_positions(word, center, font):
        width = sum(font.size(c)[0] for c in word)
        x = center[0] - width // 2
        positions = []
        for c in word:
            w, h = font.size(c)
            positions.append((x, center[1] - h // 2))
            x += w
        return positions

    def get_exit_vector():
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 5)
        return pygame.Vector2(math.cos(angle), math.sin(angle)) * speed

    class Letter:
        def __init__(self, char, final_pos, font):
            self.char = char
            self.final_pos = pygame.Vector2(final_pos)
            angle = random.uniform(0, 2 * math.pi)
            distance = max(screen.get_width(), screen.get_height()) * 1.2
            self.pos = pygame.Vector2(
                CENTER[0] + math.cos(angle) * distance,
                CENTER[1] + math.sin(angle) * distance
            )
            self.surface = font.render(char, True, (255, 255, 255))
            self.exit_velocity = get_exit_vector()
            self.departing = False

        def update(self):
            if not self.departing:
                direction = self.final_pos - self.pos
                if direction.length_squared() < 2:
                    self.pos = self.final_pos
                else:
                    self.pos += direction * 0.025
            else:
                self.pos += self.exit_velocity

        def draw(self, surface):
            surface.blit(self.surface, self.pos)

        def is_at_target(self):
            return self.pos == self.final_pos

    final_positions_main = get_final_positions(word_main, CENTER, font_main)
    final_positions_sub = get_final_positions(word_sub, (CENTER[0], CENTER[1] + 100), font_sub)

    letters = [Letter(c, pos, font_main) for c, pos in zip(word_main, final_positions_main)]
    letters += [Letter(c, pos, font_sub) for c, pos in zip(word_sub, final_positions_sub)]

    all_arrived = False
    depart_timer = 0
    fadeout = False
    fade_alpha = 0

    # Run intro loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if all_arrived and event.type == pygame.KEYDOWN:
                for l in letters:
                    l.departing = True
                fadeout = True

        screen.fill((0, 0, 0))

        all_arrived = True
        for l in letters:
            l.update()
            l.draw(screen)
            if not l.is_at_target():
                all_arrived = False

        if fadeout:
            fade_alpha += 5
            fade_surface = pygame.Surface(screen.get_size())
            fade_surface.set_alpha(min(fade_alpha, 255))
            fade_surface.fill((0, 0, 0))
            screen.blit(fade_surface, (0, 0))
            if fade_alpha >= 255:
                break

        pygame.display.flip()
        clock.tick(60)
