import pygame
import sys
from pygame.display import update

from constants import *
from player import Player, Shot
from asteroid import Asteroid
from asteroifield import AsteroidField


def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shooss = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)
    Shot.containers = (shooss, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ateroides = AsteroidField()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for upd in updatable:
            upd.update(dt)

        for ast in asteroids:
            if ast.collision(player):
                print("Game over!")
                sys.exit(0)
            for bul in shooss:
                if ast.collision(bul):
                    ast.split()
                    bul.kill()

        screen.fill((0, 0, 0, 0))

        for dra in drawable:
            dra.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
