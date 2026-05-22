from boids import Boid
import pygame
import random

WIDTH, HEIGHT = 1000, 700
NUM_BOIDS = 50
BOID_COLOR = (200, 230, 255)
BG_COLOR = (20, 24, 35)

MAX_SPEED = 4.0
MAX_FORCE = 0.1
PERCEPTION_RADIUS = 50.0
SEPARATION_DISTANCE = 25.0

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