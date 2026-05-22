from boids import Boid
from constants import WIDTH, HEIGHT, NUM_BOIDS, BG_COLOR  
import pygame
import random
import sys


def main():
    pygame.init()
    screen = pygame.display.set_name = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()
    
    flock = [Boid(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(NUM_BOIDS)]

    running = True
    while running:
        clock.tick(60) # Cap at 60 FPS
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update and draw boids
        for boid in flock:
            boid.flock(flock) # Calculate rules
            boid.update()     # Move
            boid.edges()      # Teleport if out of bounds
            boid.draw(screen) # Render

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()