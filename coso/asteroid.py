from types import new_class
import pygame
import random
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return None
        angle1 = random.uniform(20, 50)
        vector1 = self.velocity.rotate(angle1)
        vector2 = self.velocity.rotate(-angle1)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        ast1 = Asteroid(self.position[0], self.position[1], new_radius)
        ast2 = Asteroid(self.position[0], self.position[1], new_radius)

        ast1.velocity = vector1 * 1.2
        ast2.velocity = vector2 * 1.2

        return None
