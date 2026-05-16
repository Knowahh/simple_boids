import pygame
import numpy as np
import random
import sys

WIDTH, HEIGHT = 1000, 700
NUM_BOIDS = 50
BOID_COLOR = (200, 230, 255)
BG_COLOR = (20, 24, 35)

MAX_SPEED = 4.0
MAX_FORCE = 0.1
PERCEPTION_RADIUS = 50.0
SEPARATION_DISTANCE = 25.0

class Boid:
    def __init__(self, x, y):
        # Position, velocity, and acceleration as 2D vectors
        self.position = np.array([float(x), float(y)])
        
        # Random initial velocity vector
        angle = random.uniform(0, 2 * np.pi)
        self.velocity = np.array([np.cos(angle), np.sin(angle)]) * random.uniform(1, MAX_SPEED)
        self.acceleration = np.zeros(2)

    def update(self):
        # Physics update: Velocity changes by acceleration, position by velocity
        self.velocity += self.acceleration
        # Limit speed so they don't blast off into infinite velocity
        speed = np.linalg.norm(self.velocity)
        if speed > MAX_SPEED:
            self.velocity = (self.velocity / speed) * MAX_SPEED
            
        self.position += self.velocity
        # Reset acceleration for the next frame
        self.acceleration = np.zeros(2)

    def apply_force(self, force):
        self.acceleration += force

    def edges(self):
        # Wrap around the screen borders like Pac-Man
        if self.position[0] > WIDTH: self.position[0] = 0
        elif self.position[0] < 0: self.position[0] = WIDTH
        if self.position[1] > HEIGHT: self.position[1] = 0
        elif self.position[1] < 0: self.position[1] = HEIGHT

    def flock(self, boids):
        # Calculate the 3 steering forces
        sep_force = self.separation(boids) * 1.5   # Slightly favor not crashing
        ali_force = self.alignment(boids) * 1.0
        coh_force = self.cohesion(boids) * 1.0

        # Apply forces to the boid
        self.apply_force(sep_force)
        self.apply_force(ali_force)
        self.apply_force(coh_force)

    def seek(self, target):
        # Steering = Desired Velocity - Current Velocity
        desired = target - self.position
        dist = np.linalg.norm(desired)
        if dist > 0:
            desired = (desired / dist) * MAX_SPEED
            steering = desired - self.velocity
            # Limit the steering force
            steer_mag = np.linalg.norm(steering)
            if steer_mag > MAX_FORCE:
                steering = (steering / steer_mag) * MAX_FORCE
            return steering
        return np.zeros(2)

    # 1. SEPARATION: Avoid crowding local flockmates
    def separation(self, boids):
        steering = np.zeros(2)
        total = 0
        for other in boids:
            if other is self:
                continue
            distance = np.linalg.norm(self.position - other.position)
            if distance < SEPARATION_DISTANCE and distance > 0:
                # Vector pointing away from neighbor, weighted by closeness
                diff = self.position - other.position
                diff /= distance  
                steering += diff
                total += 1
                
        if total > 0:
            steering /= total
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * MAX_SPEED
                steering -= self.velocity
                if np.linalg.norm(steering) > MAX_FORCE:
                    steering = (steering / np.linalg.norm(steering)) * MAX_FORCE
        return steering

    # 2. ALIGNMENT: Steer towards average heading of local flockmates
    def alignment(self, boids):
        avg_velocity = np.zeros(2)
        total = 0
        for other in boids:
            if other is self:
                continue
            distance = np.linalg.norm(self.position - other.position)
            if distance < PERCEPTION_RADIUS:
                avg_velocity += other.velocity
                total += 1
                
        if total > 0:
            avg_velocity /= total
            avg_velocity = (avg_velocity / np.linalg.norm(avg_velocity)) * MAX_SPEED
            steering = avg_velocity - self.velocity
            if np.linalg.norm(steering) > MAX_FORCE:
                steering = (steering / np.linalg.norm(steering)) * MAX_FORCE
            return steering
        return np.zeros(2)

    # 3. COHESION: Steer to move toward the average position of local flockmates
    def cohesion(self, boids):
        avg_position = np.zeros(2)
        total = 0
        for other in boids:
            if other is self:
                continue
            distance = np.linalg.norm(self.position - other.position)
            if distance < PERCEPTION_RADIUS:
                avg_position += other.position
                total += 1
                
        if total > 0:
            avg_position /= total
            return self.seek(avg_position) # Seek that center point
        return np.zeros(2)

    def draw(self, screen):
        # Draw the boid as a small circle (you can upgrade this to a triangle later)
        pygame.draw.circle(screen, BOID_COLOR, self.position.astype(int), 4)

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