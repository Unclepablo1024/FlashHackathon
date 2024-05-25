import pygame
import random
import math

# Configuration settings from config
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SLEEP_TIME = 0.08

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BOID_RADIUS = 10

# Constants for Boid behavior
BOID_COUNT = 50
MAX_SPEED = 4
MAX_FORCE = 0.1
SEPARATION_RADIUS = 25
ALIGNMENT_RADIUS = 50
COHESION_RADIUS = 50

# Boid class
class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.acceleration = pygame.Vector2(0, 0)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def change_color_within_radius(self, circles, radius):
        for circle in circles:
            if circle != self:  # Ensure we don't check the circle against itself
                distance = self.position.distance_to(circle.position)
                if distance <= radius:
                    circle.color = self.color

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        self.velocity = self.velocity.normalize() * MAX_SPEED
        self.acceleration *= 0
    
    def apply_force(self, force):
        self.acceleration += force
    
    def edges(self):
        if self.position.x > WINDOW_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        if self.position.y > WINDOW_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = WINDOW_HEIGHT
    
    def separation(self, boids):
        steer = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < SEPARATION_RADIUS:
                diff = self.position - boid.position
                diff /= distance
                steer += diff
                total += 1
        if total > 0:
            steer /= total
            steer = steer.normalize() * MAX_SPEED - self.velocity
            steer = steer.normalize() * MAX_FORCE
        return steer
    
    def alignment(self, boids):
        avg_velocity = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < ALIGNMENT_RADIUS:
                avg_velocity += boid.velocity
                total += 1
        if total > 0:
            avg_velocity /= total
            avg_velocity = avg_velocity.normalize() * MAX_SPEED
            steer = avg_velocity - self.velocity
            steer = steer.normalize() * MAX_FORCE
            return steer
        return pygame.Vector2(0, 0)
    
    def cohesion(self, boids):
        center_of_mass = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < COHESION_RADIUS:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            direction_to_com = center_of_mass - self.position
            direction_to_com = direction_to_com.normalize() * MAX_SPEED
            steer = direction_to_com - self.velocity
            steer = steer.normalize() * MAX_FORCE
            return steer
        return pygame.Vector2(0, 0)
    
    def flock(self, boids):
        sep = self.separation(boids)
        ali = self.alignment(boids)
        coh = self.cohesion(boids)
        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), BOID_RADIUS)

# Game class
class Game:
    def __init__(self) -> None:
        pygame.init()
        self.running = True
        pygame.display.set_caption("Boids")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.surface.fill(WHITE)
        self.boids = [Boid(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(BOID_COUNT)]

    def run(self):
        clock = pygame.time.Clock()

        def change_colors_within_radius(circles, radius):
            circles[0].change_color_within_radius(circles, radius)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.surface.fill(BLACK)
            
            for boid in self.boids:
                boid.flock(self.boids)
                boid.update()
                boid.edges()
                boid.draw(self.surface)
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

