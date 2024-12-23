import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)  # Sky blue
YELLOW = (255, 223, 0)  # Sun color

# Game variables
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 60
PIPE_GAP = 150
BIRD_WIDTH = 30
BIRD_HEIGHT = 30

# Load bird image
bird_image = pygame.image.load("C:/Users/Yahya/Desktop/My folder/Programming/Python/python_projects/FlappyBird/flappy-bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def draw(self):
        SCREEN.blit(bird_image, (self.x, self.y))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)

    def draw(self):
        # Top pipe (green)
        pygame.draw.rect(SCREEN, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # Bottom pipe (green)
        pygame.draw.rect(SCREEN, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP))

    def update(self):
        self.x -= 5

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

# Function to draw the background (sky, sun, and clouds)
def draw_background():
    # Fill the screen with sky blue
    SCREEN.fill(BLUE)

    # Draw the sun
    pygame.draw.circle(SCREEN, YELLOW, (350, 100), 50)

    # Draw some clouds
    draw_cloud(50, 100)
    draw_cloud(150, 150)
    draw_cloud(300, 80)

# Function to draw a cloud (as an ellipse)
def draw_cloud(x, y):
    pygame.draw.ellipse(SCREEN, WHITE, (x, y, 100, 40))
    pygame.draw.ellipse(SCREEN, WHITE, (x + 20, y - 20, 100, 50))
    pygame.draw.ellipse(SCREEN, WHITE, (x + 50, y, 100, 40))

# Main game function
def game_loop():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]   
    running = True

    while running:
        clock.tick(30)

        # Draw background (sky, sun, clouds)
        draw_background()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Bird update
        bird.update()

        # Pipe update
        for pipe in pipes:
            pipe.update()
            pipe.draw()

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        # Add new pipes
        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe())

        # Draw bird
        bird.draw()

        # Collision detection
        for pipe in pipes:
            if (bird.x + BIRD_WIDTH > pipe.x and bird.x < pipe.x + PIPE_WIDTH and
                (bird.y < pipe.height or bird.y + BIRD_HEIGHT > pipe.height + PIPE_GAP)):
                running = False

        # Check if bird hit the ground or went off-screen
        if bird.y + BIRD_HEIGHT > SCREEN_HEIGHT or bird.y < 0:
            running = False

        pygame.display.update()

    pygame.quit()

# Start the game
game_loop()
