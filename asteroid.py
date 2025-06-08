from circleshape import *
from constants import *
import random 

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        

        new_asteroid = self.radius - ASTEROID_MIN_RADIUS

    def draw(self, screen, width = 2):
        pygame.draw.circle(screen, "white", self.position, self.radius, width = 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_screen()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            new_asteroid = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_asteroid)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_asteroid)
            # ... inside the split method, after calculating new_asteroid ...
            random_angle = random.uniform(20, 50)
            rotated_velocity1 = self.velocity.rotate(random_angle) * 1.2
            asteroid1.velocity = rotated_velocity1
            # ... do the same for asteroid2 ...
            rotated_velocity2 = self.velocity.rotate(-random_angle) * 1.2
            asteroid2.velocity = rotated_velocity2
        
    def wrap_screen(self):
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
