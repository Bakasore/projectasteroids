# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroid = pygame.sprite.Group()
    shot = pygame.sprite.Group()
    Player.containers = updatable, drawable
    Asteroid.containers = (asteroid, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = updatable, drawable, shot

    asteroidfield = AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shot)

    

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        dt = clock.tick(60) / 1000
        
        updatable.update(dt)

        for aster in asteroid:
            for bullet in shot:
                if bullet.collision_check(aster):
                    bullet.kill()
                    aster.split()

        for aster in asteroid:
            if player.collision_check(aster):
                print("Game over!")
                sys.exit() 

        for sprite in drawable:
            sprite.draw(screen)

        pygame.display.flip()
        

if __name__ == "__main__":
    main()